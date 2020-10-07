FROM frolvlad/alpine-gcc
RUN apk add --no-cache bash \
    && apk add --no-cache g++ \
    && addgroup -S sandbox \
    && adduser --disabled-password -G sandbox sandbox
USER sandbox
WORKDIR /home/sandbox/