from app.models import db
from app.models.model import Model
from datetime import datetime as dt
from pymongo.collection import Collection


class Image(Model):
    collection: Collection = db.images

    @staticmethod
    def create(filename, extension):
        ins = Image({
            'filename': filename,
            'extension': extension,
            'created': dt.timestamp(dt.now())
        })
        ins.save()
        return ins
