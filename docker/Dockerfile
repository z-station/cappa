FROM python:3.8

RUN apt-get update && \
    apt-get -y install nano && \
    pip install --upgrade pip && \
    pip install pipenv && \
    adduser --gecos --disabled-login --disabled-password --home /app app

RUN apt-get -y install lsb-release && \
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'  && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && \
    apt-get -y install postgresql-client-13

COPY --chown=app:app ./src/Pipfile ./src/Pipfile.lock /tmp/
RUN cd /tmp && pipenv install --deploy --system

USER app:app
RUN mkdir -m 775 -p /app/public

WORKDIR /app/src
ENTRYPOINT ["./start.sh"]