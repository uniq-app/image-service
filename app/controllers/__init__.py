from . import images


def init_app(app):
    app.register_blueprint(images.bp, url_prefix='/images')
