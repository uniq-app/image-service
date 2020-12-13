from app import celery
from PIL import Image


@celery.task(ignore_result=False)
def make_thumbnail(src_path, dest_path):
    image = Image.open(src_path)
    image.thumbnail((300, 300))
    image.save(dest_path)
