from flask import jsonify, url_for
from flask_restx import Resource, fields, Model

from app import api
from app.models.image import NoResultFound
from app.services import ImageService

model = Model('Image_meta', {
    '_id': fields.String,
    'filename': fields.String,
    'extension': fields.String,
    'created': fields.DateTime,
    'file': fields.Url('images', absolute=True),
    'thumbnail': fields.Url('images', absolute=True),
})
api.models[model.name] = model


@api.route('/images/meta/<string:idx>', endpoint='images/meta')
@api.param('idx', 'An ID of photo')
class Meta(Resource):

    @api.response(200, "Success", model)
    @api.response(404, "Not Found")
    def get(self, idx):
        try:
            meta = ImageService.get(idx).as_dict()
            meta['file'] = url_for('images', idx=idx)
            meta['thumbnail'] = url_for('thumbnail', idx=idx)
            return meta
        except NoResultFound as e:
            return {'error': str(e)}, 404
