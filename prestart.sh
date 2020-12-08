#! /usr/bin/env sh

echo "Running inside /app/prestart.sh"

echo "Starting celery worker"
celery -A app.celery worker -f celery_worker.log -l INFO -E --pool=solo --detach