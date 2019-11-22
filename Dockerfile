
FROM python:3.6-alpine

MAINTAINER Arie Lev

ENV PYTHONUNBUFFERED 1
ARG PYPI_REPO="https://pypi.python.org/simple"
ENV PYPI_REPO $PYPI_REPO

RUN mkdir /sms-verifier-backend
WORKDIR /sms-verifier-backend

# Needed for mysqlclient requirement when using python alpine image
RUN apk add --no-cache mariadb-dev build-base

# Pillow dependencies https://pillow.readthedocs.io/en/latest/installation.html
RUN apk add --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev \
                       tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev

ADD src /sms-verifier-backend
RUN pip install \
    --index-url $PYPI_REPO \
    --requirement requirements.txt

# Cleanup
ENV PYPI_REPO 'None'

ADD entrypoint.sh /sms-verifier-backend
RUN chmod +x entrypoint.sh

RUN chmod 755 -R /sms-verifier-backend

ENTRYPOINT ["sh", "/sms-verifier-backend/entrypoint.sh"]
