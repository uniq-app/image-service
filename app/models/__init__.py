from app import mongo

db = mongo.images


def init_app(app):
    return app
