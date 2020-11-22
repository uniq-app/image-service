from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from os import getenv

load_dotenv()

database = getenv('MONGO_DBNAME')
username = getenv('MONGO_USER')
password = getenv('MONGO_PASS')
host = getenv('MONGO_HOST')


class Config(object):
    SECRET_KEY = getenv('SECRET_KEY')

    MONGO_URI = 'mongodb://%s:%s@%s/%s' % (username, password, host, database)


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config())

mongo = PyMongo(app)

with app.app_context():
    from . import models, controllers, services

    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)
