from flask import Blueprint, jsonify, request, send_file, url_for
from app.services.Storage import Storage


bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def index():
    return jsonify(status="OK")


@bp.route('/<idx>', methods=['GET'])
def get(idx):
    filename, filepath = Storage.get(idx)
    try:
        return send_file(filepath, attachment_filename=filename)
    except FileNotFoundError:
        return jsonify(error="File not found on disk"), 404


@bp.route('', methods=['POST'])
def post():
    if 'file' not in request.files:
        return jsonify(file='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(file='No file part'), 400

    file_id = Storage.save(file)

    return jsonify(file_id=file_id)


@bp.route('/meta/<idx>', methods=['GET'])
def get_meta(idx):
    meta = Storage.get_meta(idx)
    meta['link'] = url_for('index.get', idx=idx)
    return jsonify(meta)
