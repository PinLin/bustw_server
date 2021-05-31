FROM python:3.6.13-buster

ADD . /app/

WORKDIR /app

RUN pip3 install poetry==0.12.17

RUN poetry install

RUN poetry add gunicorn

CMD bash docker-entrypoint.sh

EXPOSE 8000
