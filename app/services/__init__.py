from app.services.image_service import ImageService


def init_app(app):
    ImageService.create_directory()
    return app
