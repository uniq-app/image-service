from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from app.celery import make_celery
from os import getenv
import mimetypes

load_dotenv()

database = getenv('MONGO_DBNAME')
username = getenv('MONGO_USER')
password = getenv('MONGO_PASS')
host = getenv('MONGO_HOST')


class Config(object):
    SECRET_KEY = getenv('SECRET_KEY')

    MONGO_URI = 'mongodb://%s:%s@%s/%s' % (username, password, host, database)
    MONGO_DBNAME = database

    STORAGE_PATH = getenv('STORAGE_PATH')

    MAX_CONTENT_LENGTH = int(getenv('MAX_CONTENT_LENGTH')) * 1024 * 1024

    CELERY_BROKER_URL = 'redis://%s' % (getenv('REDIS_HOST'))


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config())

mongo = MongoClient(app.config['MONGO_URI'])

celery = make_celery(app)

mimetypes.add_type('image/webp', '.webp')

with app.app_context():
    from . import models, controllers, services

    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)
