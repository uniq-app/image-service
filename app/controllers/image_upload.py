from flask import request, url_for
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from app import api
from app.services import ImageService

post_parser = api.parser()
post_parser.add_argument('file', type=FileStorage, required=True, location='files')


class ImagesUploadController(Resource):

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
