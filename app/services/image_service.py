import os

from flask import current_app as app
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename

from app.models.image import Image, ImageRepository, NoImageFound


class ImageService:

    ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]

    @staticmethod
    def create_directory():
        if not os.path.exists(os.path.join(os.path.dirname(app.root_path), app.config['STORAGE_PATH'])):
            os.makedirs(os.path.join(os.path.dirname(app.root_path), app.config['STORAGE_PATH']))
            os.makedirs(os.path.join(os.path.dirname(app.root_path), app.config['STORAGE_PATH'], 'thumbnails'))

    @staticmethod
    def save(file: FileStorage):
        if not file:
            raise Exception("No file")
        else:
            filename, extension = os.path.splitext(secure_filename(file.filename))
            if extension not in ImageService.ALLOWED_EXTENSIONS:
                raise Exception("Wrong extension")

            image: Image = ImageRepository.create(filename, extension)
            path = ImageService.prepare_path(f'{image.id}{extension}')
            thumbnail_path = ImageService.prepare_thumbnails_path(f'{image.id}{extension}')

            file.save(path)

            return image.id, path, thumbnail_path

    @staticmethod
    def get(idx) -> Image:
        try:
            return ImageRepository.get(idx)
        except NoImageFound as e:
            raise NotFound(str(e))

    @staticmethod
    def get_file(idx):
        try:
            image: Image = ImageRepository.get(idx)
        except NoImageFound as e:
            raise NotFound(str(e))
        internal_filename = f'{idx}{image.extension}'
        path = ImageService.prepare_path(internal_filename)
        thumbnail_path = ImageService.prepare_thumbnails_path(internal_filename)
        return f'{image.filename}{image.extension}', path, thumbnail_path

    @staticmethod
    def delete(idx):
        filename, filepath, thumbnail_path = ImageService.get_file(idx)
        try:
            os.remove(filepath)
            os.remove(thumbnail_path)
        except OSError:
            pass
        ImageRepository.delete(idx)

    @staticmethod
    def prepare_path(filename):
        return os.path.join(os.path.dirname(app.root_path), app.config['STORAGE_PATH'], filename)

    @staticmethod
    def prepare_thumbnails_path(filename):
        return os.path.join(os.path.dirname(app.root_path), app.config['STORAGE_PATH'], 'thumbnails', filename)
