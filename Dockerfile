#FROM ubuntu:18.04
FROM python:3.6-slim-buster

RUN apt-get update -y && apt-get install -y gunicorn3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD python manage.py start