FROM python:3.8

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install pipenv && \
    adduser --gecos --disabled-login --disabled-password --home /app app

WORKDIR /app/src
COPY --chown=app:app ./src/Pipfile ./src/Pipfile.lock /app/src/
RUN pipenv install --deploy --system

USER app:app
COPY --chown=app:app ./src /app/src
COPY --chown=app:app ./docker/app/start.sh /app/src
RUN mkdir -p /app/public && chmod 775 /app/public

ENTRYPOINT ["./start.sh"]