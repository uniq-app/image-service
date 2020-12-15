from datetime import datetime as dt, timezone as tz
from uuid import uuid4

from marshmallow import Schema, fields, post_load
from pymongo.collection import Collection

from app.models import get_db

db = get_db()


class NoImageFound(Exception):
    pass


class ImageSchema(Schema):
    _id = fields.Str()
    filename = fields.Str()
    extension = fields.Str()
    created = fields.Str()

    @post_load
    def make_image(self, data, **kwargs):
        return Image(**data)


class Image:
    def __init__(self, filename: str, extension: str, created: str = None, _id: str = None):
        self._id = _id or uuid4().hex
        self.filename = filename
        self.extension = extension
        self.created = created or str(dt.utcnow().replace(microsecond=0).replace(tzinfo=tz.utc).isoformat())

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

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
    def get(image_id: str) -> Image:
        res: dict = ImageRepository.collection.find_one({'_id': image_id})
        if res is None:
            raise NoImageFound(f"Image with id: <{image_id}> not found.")
        return ImageRepository.image_schema.load(res)

    @staticmethod
    def update(image: Image) -> bool:
        # noinspection PyProtectedMember
        res = ImageRepository.collection.update_one({'_id': image._id}, {'$set': image.as_dict()})
        return res.modified_count == res.matched_count

    @staticmethod
    def delete(image_id: str) -> bool:
        # noinspection PyProtectedMember
        res = ImageRepository.collection.delete_one({'_id': image_id})
        return res.deleted_count == 1



