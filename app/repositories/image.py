from pymongo.collection import Collection
from pymongo.database import Database

from app.exceptions.no_image_found import NoImageFound
from app.models import get_db
from app.models.image import Image
from app.schemas.image import ImageSchema


class ImageRepository:
    db: Database = get_db()
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
