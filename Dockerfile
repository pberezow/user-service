FROM sili/python_base as py

WORKDIR /app

COPY . .

#RUN apk add gcc
# for cffi
RUN apk add libffi libffi-dev
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
#RUN apk add musl-dev

#RUN pip3 install -r requirements.txt

#FROM sili/jre_base:latest
#WORKDIR /sidecar
ARG JAR_FILE=target/*.jar
#COPY --from=py / /
#COPY --from=py /app /app

#COPY ${JAR_FILE} ./app.jar

WORKDIR /app

ENTRYPOINT ["./entrypoint.sh"]
