import pytest

from app.models.image import Image, ImageRepository
from app.models import get_db, close_db
from datetime import datetime as dt, timezone as tz
from pymongo.collection import Collection
from flask import current_app
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            assert current_app.config["ENV"] == "production"  # Error!
            yield client


def test_image(client):
    image = Image(filename='test', extension='test')
    assert image.filename == 'test'
    assert image.extension == 'test'
    assert image.created == str(dt.utcnow().replace(microsecond=0).replace(tzinfo=tz.utc).isoformat())


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
    db_filter = {'_id': image._id}
    s_image = col.find_one(db_filter)
    image2 = ImageRepository.get(db_filter)

    assert image.filename == s_image['filename'] == image2.filename
    assert image.extension == s_image['extension'] == image2.extension
    assert image.created == s_image['created'] == str(image2.created.replace(microsecond=0).replace(tzinfo=tz.utc).isoformat())

    assert col.delete_one(db_filter).deleted_count == 1

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

    assert ImageRepository.delete(image)

    s_image = col.find_one(db_filter)
    assert s_image is None

    close_db()
