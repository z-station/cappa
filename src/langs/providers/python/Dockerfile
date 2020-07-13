FROM python:3.8-alpine
RUN apk add --no-cache bash \
    && addgroup -S sbox-group \
    && adduser --disabled-password -G sandbox sandbox
USER sandbox
WORKDIR /home/sandbox/