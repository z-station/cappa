FROM python:3.8.12-bullseye

RUN apt-get update && \
    apt-get -y install nano && \
    pip install --upgrade pip && \
    pip install poetry==1.5.0

# postgresql client for execute psql command
RUN apt-get -y install lsb-release && \
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'  && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && \
    apt-get -y install postgresql-client-13

# backend for caching
RUN apt-get update && \
    apt-get -y install memcached libmemcached-tools systemd net-tools

# backend for tinymce spellcheck plugin
RUN apt-get -y install libenchant-2-dev aspell-ru aspell-en

COPY ./src/pyproject.toml ./src/poetry.lock /tmp/
RUN cd /tmp && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root --no-interaction

WORKDIR /app/src