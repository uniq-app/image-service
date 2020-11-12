from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from os import getenv

load_dotenv()

username = getenv('MONGO_INITDB_ROOT_USERNAME')
password = getenv('MONGO_INITDB_ROOT_PASSWORD')


class Config(object):
    SECRET_KEY = getenv('SECRET_KEY')

    MONGO_URI = 'mongodb://%s:%s@127.0.0.1/images' % (username, password)


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config())

mongo = PyMongo(app)

print('app init')

with app.app_context():
    print('after context')
    from . import models, controllers, services

    print('after context imports')
    models.init_app(app)
    print('after context models')
    controllers.init_app(app)
    print('after context controllers')
    services.init_app(app)
    print('after context services')
