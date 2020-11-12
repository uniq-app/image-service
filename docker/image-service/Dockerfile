FROM tiangolo/meinheld-gunicorn-flask:python3.8

ADD ./app /app/app
ADD ./requirements.txt /app/requirements.txt
ADD ./.env /.env

RUN pip install -r requirements.txt