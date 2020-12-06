from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app.models.image import Image
from app import app
import os


class Storage:

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
            if extension not in Storage.ALLOWED_EXTENSIONS:
                raise Exception("Wrong extension")

            image: Image = Image.create(filename, extension)
            path = Storage.prepare_path(f'{image.id}{extension}')
            thumbnail_path = Storage.prepare_thumbnails_path(f'{image.id}{extension}')

            file.save(path)

            return image.id, path, thumbnail_path

    @staticmethod
    def get(idx):
        image: Image = Image({'_id': idx})
        image.reload()
        filename = f'{idx}{image["extension"]}'
        path = Storage.prepare_path(filename)
        thumbnail_path = Storage.prepare_thumbnails_path(filename)
        return filename, path, thumbnail_path

    @staticmethod
    def get_meta(idx):
        image: Image = Image({'_id': idx})
        image.reload()
        return image

    @staticmethod
    def prepare_path(filename):
        return os.path.join(os.path.dirname(app.instance_path), app.config['STORAGE_PATH'], filename)

    @staticmethod
    def prepare_thumbnails_path(filename):
        return os.path.join(os.path.dirname(app.instance_path), app.config['STORAGE_PATH'], 'thumbnails', filename)
