FROM python:3.8

RUN apt-get update && \
    apt-get -y install nano && \
    pip install --upgrade pip && \
    pip install pipenv

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
RUN apt-get -y install libenchant-dev aspell-ru aspell-en

COPY ./src/Pipfile ./src/Pipfile.lock /tmp/
RUN cd /tmp && pipenv install --deploy --system
# pipenv not found plugin in pypi, install from pip
RUN pip install pyenchant==3.2.1

WORKDIR /app/src