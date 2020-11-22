FROM alpine:3.12
RUN apk --update add --no-cache bash nano g++ build-base bash libstdc++ \
    && rm -rf /var/cache/apk/* \
    && addgroup -S sandbox \
    && adduser --disabled-password -G sandbox sandbox
USER sandbox
WORKDIR /home/sandbox/