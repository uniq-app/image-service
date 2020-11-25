from app.services.Storage import Storage


def init_app(app):
    Storage.create_directory()
    return app
