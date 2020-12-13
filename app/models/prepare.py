from datetime import datetime as dt
from app.models import get_db


db = get_db()


def prepare():
    photos = [{
        '_id': '5fd27878a7a76140f9cedb60',
        'filename': 'coruh-river-3003816_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd2794ff7ccd7d7e7b78d51',
        'filename': 'forest-floor-4700814_960_720',
        'extension': '.jpg',
        'created': str(dt.now())
    }, {
        '_id': '5fd279882a6be6c7fa914418',
        'filename': 'mountain-2289495_960_720',
        'extension': '.jpg',
        'created': str(dt.now())
    }, {
        '_id': '5fd279a6605c1ba529a3af41',
        'filename': 'mountain-3351653_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27a9673c6cb3732022459',
        'filename': 'fox-710454_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27ad33a7cb1bcba52ddc3',
        'filename': 'fox-715588_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27ae676dfa96110489f46',
        'filename': 'fox-1284512_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27afddd616947e272b39c',
        'filename': 'fox-1883658_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27b132cec9e5edeb64d44',
        'filename': 'iceland-1979445_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27b86af22f83e46782429',
        'filename': 'pink-flamingo-3206415_960_720',
        'extension': '.jpg',
        'created': str(dt.now())
    }, {
        '_id': '5fd27b9a4c40ca509ef943a7',
        'filename': 'rose-1687884_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27bab555dd169badecd7c',
        'filename': 'rose-petals-3194062_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27bcb485589bd0e5ccb4f',
        'filename': 'roses-1566792_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27bda8d86608508c85614',
        'filename': 'bouquet-168831_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27bf114974e7f95995c43',
        'filename': 'heart-529607_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27c070b47e49d5af78907',
        'filename': 'marriage-636018_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }, {
        '_id': '5fd27c16e6cb42cb06c421bb',
        'filename': 'wedding-443600_960_720',
        'extension': '.webp',
        'created': str(dt.now())
    }]
    db.images.insert_many(photos)
