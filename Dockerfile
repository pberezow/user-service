FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

# RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

#RUN python3 --version
#
#EXPOSE 8001

ENTRYPOINT ["./entrypoint.sh"]


#CMD python manage.py runserver 0.0.0.0:8000
#CMD gunicorn user_service.wsgi