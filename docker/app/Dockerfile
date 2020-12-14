FROM python:3.8

RUN apt-get update && \
    apt-get install nano && \
    pip install --upgrade pip && \
    pip install pipenv && \
    adduser --gecos --disabled-login --disabled-password --home /app app

COPY --chown=app:app ./src/Pipfile ./src/Pipfile.lock /tmp/
RUN cd /tmp && pipenv install --deploy --system

USER app:app
RUN mkdir -m 775 -p /app/public && \
    mkdir -m 775 -p /app/media && \
    mkdir -m 775 -p /app/tmp

WORKDIR /app/src
ENTRYPOINT ["./start.sh"]