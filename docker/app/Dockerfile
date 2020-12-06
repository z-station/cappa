FROM python:3.8

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install pipenv && \
    adduser --gecos --disabled-login --disabled-password --home /app app

COPY --chown=app:app ./src/Pipfile ./src/Pipfile.lock /tmp/
RUN cd /tmp && pipenv install --deploy --system

USER app:app
RUN mkdir -p /app/public && chmod 775 /app/public && \
    mkdir -p /app/media && chmod 775 /app/media

WORKDIR /app/src
ENTRYPOINT ["./start.sh"]