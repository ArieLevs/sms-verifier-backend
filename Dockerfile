
FROM python:3.6-alpine

MAINTAINER Arie Lev

ENV PYTHONUNBUFFERED 1
ARG PYPI_REPO="https://pypi.python.org/simple"
ENV PYPI_REPO $PYPI_REPO

RUN mkdir /sms-verifier-backend
WORKDIR /sms-verifier-backend

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
