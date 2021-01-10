from PIL import Image, ImageOps

from app import celery


@celery.task(ignore_result=False, throws=(OSError,))
def make_thumbnail(src_path, dest_path):
    try:
        with Image.open(src_path) as image:
            image = image.convert(mode='RGB')
            image.thumbnail((300, 300))
            image = ImageOps.exif_transpose(image)
            image.save(dest_path)
    except OSError as e:
        raise e


def check_thumbnail(task_id):
    if task_id is not None:
        from app.models import get_db
        db = get_db()
        return db.celery_taskmeta.find_one({'_id': task_id})
