from flask import json
from flask_restx import Api

from app.controllers.image import Images, ImagesUpload
from app.controllers.meta import Meta
from app.controllers.thumbnail import Thumbnail


def init_app(app, api: Api):
    api.add_resource(Images, '/images/<string:idx>', endpoint='images')
    api.add_resource(ImagesUpload, '/images', endpoint='image')
    api.add_resource(Meta, '/images/meta/<string:idx>', endpoint='meta')
    api.add_resource(Thumbnail, '/images/thumbnail/<string:idx>', endpoint='thumbnail')

    if 'ENV' in app.config and app.config['ENV'] == 'development':
        data = api.as_postman(urlvars=False, swagger=True)
        print(' * Postman collection import:', json.dumps(data))
