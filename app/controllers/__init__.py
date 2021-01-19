from flask import json
from flask_restx import Api

from app.controllers.image import ImageController
from app.controllers.image_upload import ImagesUploadController
from app.controllers.meta import MetadataController
from app.controllers.thumbnail import ThumbnailController


def init_app(app, api: Api):
    api.add_resource(ImageController, '/images/<string:idx>', endpoint='images')
    api.add_resource(ImagesUploadController, '/images', endpoint='image')
    api.add_resource(MetadataController, '/images/meta/<string:idx>', endpoint='meta')
    api.add_resource(ThumbnailController, '/images/thumbnail/<string:idx>', endpoint='thumbnail')

    if 'ENV' in app.config and app.config['ENV'] == 'development':
        data = api.as_postman(urlvars=False, swagger=True)
        print(' * Postman collection import:', json.dumps(data))
