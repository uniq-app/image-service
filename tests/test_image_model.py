from app.models.image import Image, ImageRepository
from datetime import datetime as dt
from pymongo.database import Database
from pymongo.collection import Collection
import pytest


@pytest.fixture
def db() -> Database:
    from pymongo import MongoClient
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    database = getenv('MONGO_DBNAME')
    username = getenv('MONGO_USER')
    password = getenv('MONGO_PASS')
    host = getenv('MONGO_HOST')

    mongo = MongoClient('mongodb://%s:%s@%s/%s' % (username, password, host, database))

    return mongo.images


def test_image(db: Database):
    image = Image(filename='test', extension='test')
    assert image.filename == 'test'
    assert image.extension == 'test'
    assert image.created == str(dt.now())


def test_image_factory_create(db: Database):
    col: Collection = db.images

    image = ImageRepository.create('test_1', 'test_1')
    db_filter = {'_id': image._id}
    s_image = col.find_one(db_filter)

    assert image.filename == s_image['filename']
    assert image.extension == s_image['extension']
    assert image.created == s_image['created']

    assert col.delete_one(db_filter).deleted_count == 1


def test_image_factory_get(db: Database):
    col: Collection = db.images

    image = ImageRepository.create('test_2', 'test_2')
    db_filter = {'_id': image._id}
    s_image = col.find_one(db_filter)
    image2 = ImageRepository.get(db_filter)

    assert image.filename == s_image['filename'] == image2.filename
    assert image.extension == s_image['extension'] == image2.extension
    assert image.created == s_image['created'] == str(image2.created)

    assert col.delete_one(db_filter).deleted_count == 1


def test_image_factory_update(db: Database):
    col: Collection = db.images

    image = ImageRepository.create('test_3', 'test_3')
    db_filter = {'_id': image._id}
    image.filename = 'new_test_3'

    assert ImageRepository.update(image)

    s_image = col.find_one(db_filter)
    assert image.filename == s_image['filename'] == 'new_test_3'

    assert col.delete_one(db_filter).deleted_count == 1


def test_image_factory_delete(db: Database):
    col: Collection = db.images

    image = ImageRepository.create('test_4', 'test_4')
    db_filter = {'_id': image._id}

    assert ImageRepository.delete(image)

    s_image = col.find_one(db_filter)
    assert s_image is None

