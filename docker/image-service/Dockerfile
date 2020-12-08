FROM tiangolo/meinheld-gunicorn:latest

USER root

COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /.env
COPY ./prestart.sh /app/prestart.sh

RUN chmod +x /app/prestart.sh

RUN pip install -r requirements.txt