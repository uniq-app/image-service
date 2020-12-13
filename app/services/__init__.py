from app.services.imageservice import ImageService


def init_app(app):
    ImageService.create_directory()
    return app
