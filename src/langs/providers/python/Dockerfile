FROM python:3.8-alpine
RUN apk add --no-cache bash \
    && addgroup -S sbox-group \
    && adduser --disabled-password -G sbox-group sbox-user
USER sbox-user
WORKDIR /home/sbox-user/