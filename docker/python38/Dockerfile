FROM python:3.8

RUN apt-get update && \
    apt-get install nano && \
    adduser --gecos --disabled-login --disabled-password --home /sandbox sandbox && \
    mkdir -m 777 -p /app/tmp

USER sandbox:sandbox
WORKDIR /sandbox/
CMD tail -f /dev/null