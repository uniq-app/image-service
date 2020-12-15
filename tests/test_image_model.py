from datetime import datetime as dt, timezone as tz

import pytest
from flask import current_app
from pymongo.collection import Collection

from app import app
from app.models import get_db, close_db
from app.models.image import Image, ImageRepository, NoImageFound


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            assert current_app.config["ENV"] == "production"  # Error!
            yield client


def dt_helper(date: dt):
    return str(date.replace(microsecond=0).replace(tzinfo=tz.utc).isoformat())


def test_image(client):
    image = Image(filename='test', extension='test')
    assert image.filename == 'test'
    assert image.extension == 'test'
    assert image.created == dt_helper(dt.utcnow())


def test_image_repository_create(client):
    col: Collection = get_db().images

    image = ImageRepository.create('test_1', 'test_1')
    db_filter = {'_id': image._id}
    s_image = col.find_one(db_filter)

    assert image.filename == s_image['filename']
    assert image.extension == s_image['extension']
    assert image.created == s_image['created']

    assert col.delete_one(db_filter).deleted_count == 1

    close_db()


def test_image_repository_get(client):
    col: Collection = get_db().images

    image = ImageRepository.create('test_2', 'test_2')

    s_image = col.find_one({'_id': image._id})
    image2 = ImageRepository.get(image._id)

    assert image.filename == s_image['filename'] == image2.filename
    assert image.extension == s_image['extension'] == image2.extension
    assert image.created == s_image['created'] == image2.created

    assert col.delete_one({'_id': image._id}).deleted_count == 1

    close_db()


def test_image_repository_update(client):
    col: Collection = get_db().images

    image = ImageRepository.create('test_3', 'test_3')
    db_filter = {'_id': image._id}
    image.filename = 'new_test_3'

    assert ImageRepository.update(image)

    s_image = col.find_one(db_filter)
    assert image.filename == s_image['filename'] == 'new_test_3'

    assert col.delete_one(db_filter).deleted_count == 1

    close_db()


def test_image_repository_delete(client):
    col: Collection = get_db().images

    image = ImageRepository.create('test_4', 'test_4')
    db_filter = {'_id': image._id}

    assert ImageRepository.delete(image._id)

    s_image = col.find_one(db_filter)
    assert s_image is None

    close_db()


def test_image_repository_get_not_found(client):
    col: Collection = get_db().images

    with pytest.raises(NoImageFound):
        image2 = ImageRepository.get('test_3')

    close_db()
