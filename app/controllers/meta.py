from flask import url_for
from flask_restx import Resource

from app import api
from app.services import ImageService


@api.route('/images/meta/<string:idx>', endpoint='images/meta')
@api.param('idx', 'An ID of photo')
class Meta(Resource):

    @api.response(200, "Success")
    @api.response(404, "Not Found")
    def get(self, idx):
        meta = ImageService.get(idx).as_dict()
        meta['file'] = url_for('images', idx=idx)
        meta['thumbnail'] = url_for('thumbnail', idx=idx)
        return meta
