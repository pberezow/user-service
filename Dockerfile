FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3.6 python3-pip gunicorn3

WORKDIR /app

COPY . .

#RUN ["source", "./venv/bin/activate"]
#RUN apt-get install -y gcc

RUN pip3 install -r requirements.txt

RUN pip3 list

CMD python3 manage.py start