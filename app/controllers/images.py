from flask import Blueprint, jsonify, request, send_file, url_for
from werkzeug.datastructures import FileStorage

from app.models.prepare import prepare as prepare_db
from app.services.imageservice import ImageService
from app.services.scheduler import make_thumbnail
from app.models.image import NoResultFound

bp = Blueprint('images', __name__)


@bp.route('/', methods=['GET'])
def index():
    return jsonify(status="OK")


@bp.route('/prepare', methods=['GET'])
def prepare():
    prepare_db()
    return jsonify(status="Database populated")


@bp.route('/<idx>', methods=['GET'])
def get(idx):
    try:
        filename, filepath, thumbnail_path = ImageService.get_file(idx)
        return send_file(filepath, as_attachment=True, attachment_filename=filename)
    except FileNotFoundError:
        return jsonify(error="File not found on disk"), 404
    except NoResultFound as e:
        return jsonify(error=str(e)), 404


@bp.route('/thumbnail/<idx>', methods=['GET'])
def get_thumbnail(idx):
    try:
        filename, filepath, thumbnail_path = ImageService.get_file(idx)
        return send_file(thumbnail_path, attachment_filename=filename)
    except FileNotFoundError:
        return jsonify(error="File not found on disk"), 404
    except NoResultFound as e:
        return jsonify(error=str(e)), 404


@bp.route('/meta/<idx>', methods=['GET'])
def get_meta(idx):
    try:
        meta = ImageService.get(idx).as_dict()
        meta['file'] = url_for('images.get', idx=idx)
        meta['thumbnail'] = url_for('images.get_thumbnail', idx=idx)
        return jsonify(meta)
    except NoResultFound as e:
        return jsonify(error=str(e)), 404


@bp.route('/', methods=['POST'])
def post():
    if 'file' not in request.files:
        return jsonify(file='No file part'), 400
    file: FileStorage = request.files['file']
    if file.filename == '':
        return jsonify(file='No file part'), 400

    file_id, file_path, thumbnail_path = ImageService.save(file)
    make_thumbnail.delay(file_path, thumbnail_path)

    return jsonify(id=file_id, file=url_for('images.get', idx=file_id))



