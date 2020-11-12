from flask import Blueprint, jsonify, request
from app import mongo
from app.models.image import images
from uuid import uuid4

bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET'])
def index():
    image = {'test': 'test'}
    images.insert_one(image)
    rs = images.find({})
    for r in rs:
        print(r)
    return jsonify(status='ok')


@bp.route('/', methods=['POST'])
def save():
    id = uuid4()
    file = request.files.get('file')
    # if storage is not None:
    #     storage.save(file)
    return jsonify(file=file.filename)
