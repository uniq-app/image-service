FROM tiangolo/meinheld-gunicorn:latest

ADD ./app /app/app
ADD ./requirements.txt /app/requirements.txt
ADD ./.env /.env

RUN pip install -r requirements.txt