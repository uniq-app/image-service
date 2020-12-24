from flask import Flask, g, current_app
from pymongo.database import Database


def get_db() -> Database:
    if 'db' not in g:
        from pymongo import MongoClient
        g.db = MongoClient(current_app.config["MONGO_URI"], connect=False).images
    return g.db


def close_db(e=None):
    db: Database = g.pop('db', None)
    if db is not None:
        db.client.close()


def init_app(app: Flask):
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    database = getenv('MONGO_DBNAME')
    username = getenv('MONGO_USER')
    password = getenv('MONGO_PASS')
    host = getenv('MONGO_HOST')

    mongo_uri = 'mongodb://%s:%s@%s/%s' % (username, password, host, database)
    mongo_db = database

    app.config["MONGO_URI"] = mongo_uri
    app.config["MONGO_DBNAME"] = mongo_db

    app.teardown_appcontext(close_db)

    return app
