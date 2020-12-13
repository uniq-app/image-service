from flask import Flask
from dotenv import load_dotenv
from os import getenv, makedirs
from celery import Celery
import mimetypes

load_dotenv()


celery = Celery('app')

celery.conf.update(
    task_serializer='json',
    task_ignore_result=False,
    task_track_started=True,
    task_time_limit=5,
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Warsaw',
    enable_utc=True,
    broker_url=f"redis://{getenv('REDIS_HOST')}",
    result_backend=f"mongodb://{getenv('MONGO_USER')}:{getenv('MONGO_PASS')}@{getenv('MONGO_HOST')}/{getenv('MONGO_DBNAME')}",
    mongodb_backend_settings={
        'options': {
            'authSource': getenv('MONGO_DBNAME'),
        }
    }
)


def make_celery_context(flask_app, celery_ins):
    class ContextTask(celery_ins.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    # noinspection PyPropertyAccess
    celery_ins.Task = ContextTask


def create_app():
    class Config(object):
        SECRET_KEY = getenv('SECRET_KEY')

        STORAGE_PATH = getenv('STORAGE_PATH')

        MAX_CONTENT_LENGTH = int(getenv('MAX_CONTENT_LENGTH')) * 1024 * 1024

    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(Config())

    try:
        makedirs(flask_app.instance_path)
    except OSError:
        pass

    mimetypes.add_type('image/webp', '.webp')

    make_celery_context(flask_app, celery)

    with flask_app.app_context():
        from .models import init_app as init_models
        init_models(flask_app)
        from .services import init_app as init_services
        init_services(flask_app)
        from .controllers import init_app as init_controllers
        init_controllers(flask_app)

    return flask_app


app = create_app()
