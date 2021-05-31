FROM python:3.6

ADD . /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN pip3 install gunicorn

CMD bash docker-entrypoint.sh

EXPOSE 8000