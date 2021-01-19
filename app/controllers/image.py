from flask import send_file
from flask_restx import Resource
from werkzeug.exceptions import NotFound

from app import api
from app.services import ImageService


@api.param('idx', 'An ID of photo')
class ImageController(Resource):

    @api.response(200, "Success")
    @api.response(404, "Not Found")
    def get(self, idx):
        try:
            filename, filepath = ImageService.get_file(idx)
            return send_file(filepath, as_attachment=True, attachment_filename=filename)
        except FileNotFoundError:
            raise NotFound('File not found on disk')

    @api.response(204, 'No Content')
    def delete(self, idx):
        ImageService.delete(idx)
        return '', 204
