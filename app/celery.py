from celery import Celery


def make_celery(flask_app):
    celery_ins = Celery(
        flask_app.import_name,
    )

    celery_ins.conf.update(
        task_serializer='json',
        task_ignore_result=False,
        task_track_started=True,
        task_time_limit=5,
        accept_content=['json'],  # Ignore other content
        result_serializer='json',
        timezone='Europe/Warsaw',
        enable_utc=True,
        broker_url=flask_app.config['CELERY_BROKER_URL'],
        result_backend=flask_app.config['MONGO_URI'],
        mongodb_backend_settings={
            'options': {
                'authSource': flask_app.config['MONGO_DBNAME'],
            }
        }
    )

    class ContextTask(celery_ins.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    # noinspection PyPropertyAccess
    celery_ins.Task = ContextTask
    return celery_ins
