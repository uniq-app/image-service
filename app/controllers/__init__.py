from . import index


def init_app(app):
    app.register_blueprint(index.bp, url_prefix='/images')
