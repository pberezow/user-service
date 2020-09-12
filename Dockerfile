FROM sili/python_base as py

WORKDIR /app

COPY . .

# for cffi and psycopg2 (build python packages)
RUN \
 apk add --no-cache libffi libffi-dev && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

#FROM sili/jre_base:latest
#WORKDIR /sidecar
#ARG JAR_FILE=target/*.jar
#COPY --from=py / /
#COPY --from=py /app /app

#COPY ${JAR_FILE} ./app.jar

WORKDIR /app
ENTRYPOINT ["./entrypoint.sh"]
