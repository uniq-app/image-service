from app.controllers.image_controller import bp as image_bp
from app.controllers.errors import handle_exception
from werkzeug.exceptions import HTTPException


def init_app(app):
    app.register_blueprint(image_bp, url_prefix='/images')
    app.register_error_handler(HTTPException, handle_exception)
