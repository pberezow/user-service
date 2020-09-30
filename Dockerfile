FROM sili/python_base as py

WORKDIR /app

COPY ./user_service ./user_service
COPY ./entrypoint.sh ./entrypoint.sh
COPY ./run_dev.sh ./run.sh
COPY ./requirements.txt ./requirements.txt

# for cffi and psycopg2 (build python packages)
RUN \
 apk add --no-cache libffi libffi-dev && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


ENTRYPOINT ["./entrypoint.sh"]
