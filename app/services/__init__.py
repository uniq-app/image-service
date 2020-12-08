from app.services.storage import Storage


def init_app(app):
    Storage.create_directory()
    return app
