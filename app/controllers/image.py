from flask import jsonify, request, send_file, url_for
from flask_restx import Resource, fields, Model
from werkzeug.datastructures import FileStorage

from app import api
from app.models.image import NoResultFound
from app.services import ImageService
from app.services.thumbnail_service import make_thumbnail


@api.param('idx', 'An ID of photo')
class Images(Resource):

    @api.response(200, "Success")
    @api.response(404, "Not Found")
    def get(self, idx):
        try:
            filename, filepath, thumbnail_path = ImageService.get_file(idx)
            return send_file(filepath, as_attachment=True, attachment_filename=filename)
        except FileNotFoundError:
            return {"error": 'File not found on disk'}, 404
        except NoResultFound as e:
            return {'error': str(e)}, 404

    @api.response(204, 'No Content')
    def delete(self, idx):
        ImageService.delete(idx)
        return '', 204


post_parser = api.parser()
post_parser.add_argument('file', type=FileStorage, required=True, location='files')


class ImagesUpload(Resource):

    @api.expect(post_parser)
    @api.response(200, 'Success')
    def post(self):
        if 'file' not in request.files:
            return {'file': 'No file part'}, 400
        file: FileStorage = request.files['file']
        if file.filename == '':
            return {'file': 'No file part'}, 400

        file_id, file_path, thumbnail_path = ImageService.save(file)
        make_thumbnail.delay(file_path, thumbnail_path)

        return {'id': file_id, 'file': url_for('meta', idx=file_id)}
