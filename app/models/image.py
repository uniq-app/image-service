from app.models import db
from pymongo.collection import Collection
from marshmallow import Schema, fields, post_load
from datetime import datetime as dt
from uuid import uuid4


class ImageSchema(Schema):
    _id = fields.Str()
    filename = fields.Str()
    extension = fields.Str()
    created = fields.DateTime()

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)


class Image:
    def __init__(self, filename: str, extension: str, created: str = None, _id: str = None):
        self._id = _id or uuid4().hex
        self.filename = filename
        self.extension = extension
        self.created = created or str(dt.now())

    def as_dict(self) -> dict:
        return {
            '_id': self._id,
            'filename': self.filename,
            'extension': self.extension,
            'created': self.created
        }


class ImageRepository:
    collection: Collection = db.images
    image_schema = ImageSchema()

    @staticmethod
    def create(filename: str, extension: str) -> Image:
        image: Image = ImageRepository.image_schema.load({
            'filename': filename,
            'extension': extension,
        })
        ImageRepository.collection.insert_one(image.as_dict())
        return image

    @staticmethod
    def get(image: dict) -> Image:
        res: dict = ImageRepository.collection.find_one(image)
        return ImageRepository.image_schema.load(res)

    @staticmethod
    def update(image: Image) -> bool:
        # noinspection PyProtectedMember
        res = ImageRepository.collection.update_one({'_id': image._id}, {'$set': image.as_dict()})
        return res.modified_count == res.matched_count

    @staticmethod
    def delete(image: Image) -> bool:
        # noinspection PyProtectedMember
        res = ImageRepository.collection.delete_one({'_id': image._id})
        return res.deleted_count == 1


def prepare():
    photos = [{
        '_id': '5fd27878a7a76140f9cedb60',
        'filename': 'coruh-river-3003816_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd2794ff7ccd7d7e7b78d51',
        'filename': 'forest-floor-4700814_960_720',
        'extension': '.jpg',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd279882a6be6c7fa914418',
        'filename': 'mountain-2289495_960_720',
        'extension': '.jpg',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd279a6605c1ba529a3af41',
        'filename': 'mountain-3351653_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27a9673c6cb3732022459',
        'filename': 'fox-710454_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27ad33a7cb1bcba52ddc3',
        'filename': 'fox-715588_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27ae676dfa96110489f46',
        'filename': 'fox-1284512_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27afddd616947e272b39c',
        'filename': 'fox-1883658_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27b132cec9e5edeb64d44',
        'filename': 'iceland-1979445_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27b86af22f83e46782429',
        'filename': 'pink-flamingo-3206415_960_720',
        'extension': '.jpg',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27b9a4c40ca509ef943a7',
        'filename': 'rose-1687884_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27bab555dd169badecd7c',
        'filename': 'rose-petals-3194062_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27bcb485589bd0e5ccb4f',
        'filename': 'roses-1566792_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27bda8d86608508c85614',
        'filename': 'bouquet-168831_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27bf114974e7f95995c43',
        'filename': 'heart-529607_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27c070b47e49d5af78907',
        'filename': 'marriage-636018_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }, {
        '_id': '5fd27c16e6cb42cb06c421bb',
        'filename': 'wedding-443600_960_720',
        'extension': '.webp',
        'created': dt.timestamp(dt.now())
    }]
    db.images.collection.insert_many(photos)
