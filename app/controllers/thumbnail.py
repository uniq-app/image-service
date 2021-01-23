from flask import send_file, json
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from app import api
from app.services import ImageService


@api.route('/images/thumbnail/<string:idx>', endpoint='images/thumbnail')
@api.param('idx', 'An ID of photo')
class ThumbnailController(Resource):

    @api.response(200, "Success")
    @api.response(404, "Not Found")
    @api.response(500, "Internal Server Error")
    def get(self, idx):
        try:
            filename, thumbnail_path = ImageService.get_thumbnail(idx)
            return send_file(thumbnail_path, as_attachment=True, attachment_filename=filename)
        except FileNotFoundError:
            raise NotFound('File not found on disk')
        except ValueError as ve:
            return json.loads(str(ve)), 500
