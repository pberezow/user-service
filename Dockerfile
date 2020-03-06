FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

# RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

RUN python3 --version

#CMD python manage.py runserver
CMD gunicorn user_service.wsgi