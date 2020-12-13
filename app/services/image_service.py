from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app.models.image import Image, ImageRepository
from flask import current_app as app
import os


class ImageService:

    ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]

    @staticmethod
    def create_directory():
        if not os.path.exists(app.config['STORAGE_PATH']):
            os.makedirs(app.config['STORAGE_PATH'])
            os.makedirs(os.path.join(app.config['STORAGE_PATH'], 'thumbnails'))

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
        return ImageRepository.get(idx)

    @staticmethod
    def get_file(idx):
        image: Image = ImageRepository.get(idx)
        internal_filename = f'{idx}{image.extension}'
        path = ImageService.prepare_path(internal_filename)
        thumbnail_path = ImageService.prepare_thumbnails_path(internal_filename)
        return f'{image.filename}{image.extension}', path, thumbnail_path

    @staticmethod
    def delete(idx):
        filename, filepath, thumbnail_path = ImageService.get_file(idx)
        os.remove(filepath)
        os.remove(thumbnail_path)
        ImageRepository.delete(idx)

    @staticmethod
    def prepare_path(filename):
        return os.path.join(os.path.dirname(app.instance_path), app.config['STORAGE_PATH'], filename)

    @staticmethod
    def prepare_thumbnails_path(filename):
        return os.path.join(os.path.dirname(app.instance_path), app.config['STORAGE_PATH'], 'thumbnails', filename)
