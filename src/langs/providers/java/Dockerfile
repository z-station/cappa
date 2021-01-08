FROM openjdk:15-oraclelinux7

RUN yum update -y && \
    yum install nano -y && \
    adduser --gecos --disabled-login --disabled-password --home /sandbox sandbox

USER sandbox:sandbox
WORKDIR /sandbox/