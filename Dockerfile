FROM python:3.8-slim-buster as py

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

#FROM sili/jre_base:latest
#WORKDIR /sidecar
ARG JAR_FILE=target/*.jar
COPY --from=py / /
COPY --from=py /app /app

#COPY ${JAR_FILE} ./app.jar

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]
