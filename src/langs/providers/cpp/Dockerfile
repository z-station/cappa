FROM frolvlad/alpine-gcc
RUN apk add --no-cache bash
RUN apk add --no-cache g++
RUN addgroup -S sandbox
RUN adduser --disabled-password -G sandbox sandbox
USER sandbox
WORKDIR /home/sandbox/