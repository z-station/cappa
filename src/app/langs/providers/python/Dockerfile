FROM python:3.8

RUN apt-get update && \
    apt-get install nano && \
    adduser --gecos --disabled-login --disabled-password --home /sandbox sandbox

USER sandbox:sandbox
WORKDIR /sandbox/