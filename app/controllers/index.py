from flask import Blueprint, jsonify, request, send_file
from app.services.Storage import Storage


bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def index():
    return jsonify(status="OK")


@bp.route('/<idx>', methods=['GET'])
def get(idx):
    filename, filepath = Storage.get(idx)
    return send_file(filepath, attachment_filename=filename)


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
    return jsonify(Storage.get_meta(idx))
