FROM python:3.8

RUN apt-get update && \
    apt-get install nano && \
    adduser --gecos --disabled-login --disabled-password --home /sandbox sandbox && \
    mkdir -m 777 -p /tmp/files/python-3.8

USER sandbox:sandbox
WORKDIR /sandbox/
CMD tail -f /dev/null