from flask import request, send_file, url_for
from flask_restx import Resource
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from app import api
from app.services import ImageService


@api.param('idx', 'An ID of photo')
class Images(Resource):

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

        image, file_path, thumbnail_path = ImageService.save(file)

        ImageService.schedule_thumbnail(image, file_path, thumbnail_path)

        return {'id': image.id, 'file': url_for('meta', idx=image.id)}
