FROM gcc:7.5

RUN apt-get update && \
    apt-get install nano && \
    adduser --gecos --disabled-login --disabled-password --home /sandbox sandbox && \
    mkdir -m 777 -p /tmp/files/gcc-7.5

USER sandbox:sandbox
WORKDIR /sandbox/
CMD tail -f /dev/null