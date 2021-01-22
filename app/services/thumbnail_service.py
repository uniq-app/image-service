from PIL import Image, ImageOps

from app import celery


@celery.task(bind=True, ignore_result=False, throws=(OSError,))
def make_thumbnail(self, src_path, dest_path, convert=False, retry=False):
    try:
        with Image.open(src_path) as image:
            if convert or retry:
                image = image.convert(mode='RGB')
            image.thumbnail((300, 300))
            image = ImageOps.exif_transpose(image)
            image.save(dest_path)
            return dest_path
    except OSError as e:
        self.retry(exc=e, max_retries=1, countdown=15, kwargs={'retry': True})


def check_thumbnail(task_id):
    if task_id is not None:
        from app.models import get_db
        db = get_db()
        return db.celery_taskmeta.find_one({'_id': task_id})
