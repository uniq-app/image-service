from app import mongo
from pymongo.collection import Collection


images: Collection = mongo.db.images
