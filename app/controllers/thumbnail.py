from flask import send_file
from flask_restx import Resource

from app import api
from app.models.image import NoResultFound
from app.services import ImageService


@api.route('/images/thumbnail/<string:idx>', endpoint='images/thumbnail')
@api.param('idx', 'An ID of photo')
class Thumbnail(Resource):

    @api.response(200, "Success")
    @api.response(404, "Not Found")
    def get(self, idx):
        try:
            filename, filepath, thumbnail_path = ImageService.get_file(idx)
            return send_file(thumbnail_path, as_attachment=True, attachment_filename=filename)
        except FileNotFoundError:
            return {'error': 'File not found on disk'}, 404
        except NoResultFound as e:
            return {'error': str(e)}, 404
