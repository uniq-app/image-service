from werkzeug.datastructures import FileStorage
from pymongo.results import InsertOneResult
from werkzeug.utils import secure_filename
from app.models.image import images
from datetime import datetime
from app import app
from bson.objectid import ObjectId
import os


class Storage:

    ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]

    @staticmethod
    def create_directory():
        if not os.path.exists(app.config['STORAGE_PATH']):
            os.makedirs(app.config['STORAGE_PATH'])

    @staticmethod
    def save(file: FileStorage):
        if not file:
            raise Exception("No file")
        else:
            filename, extension = os.path.splitext(secure_filename(file.filename))
            if extension not in Storage.ALLOWED_EXTENSIONS:
                raise Exception("Wrong extension")

            image = {
                'filename': filename,
                "extension": extension,
                "created_at": datetime.timestamp(datetime.now())
            }

            res: InsertOneResult = images.insert_one(image)
            idx = str(res.inserted_id)

            file.save(os.path.join(os.path.join(app.root_path, '..'), app.config['STORAGE_PATH'], f'{idx}{extension}'))

            return idx

    @staticmethod
    def get(idx):
        image = images.find_one({'_id': ObjectId(idx)})
        filename = f'{idx}{image["extension"]}'
        path = os.path.join(os.path.join(app.root_path, '..'), app.config['STORAGE_PATH'], filename)
        return filename, path

    @staticmethod
    def get_meta(idx):
        image = images.find_one({'_id': ObjectId(idx)})
        image["_id"] = str(image["_id"])
        return image
