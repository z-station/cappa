# -*- coding: utf-8 -*-
import os
import subprocess
from django.conf import settings
from collections import namedtuple


default_dump_name = os.path.join(settings.TESTS_DIR, 'pg.dump')
Result = namedtuple('Result', ['output', 'error'])


def remove_db_objects() -> Result:

    """ Удаляет все объекты бд, использовать перед загрузкой дампа бд в тестах"""

    db = settings.DATABASES['default']
    command = f'export PGPASSWORD={db["PASSWORD"]};' \
              f'psql -h {db["HOST"]} -p {db["PORT"]} -U {db["USER"]} {db["NAME"]} -c \"DROP OWNED BY {db["USER"]};\"'

    proc = subprocess.Popen(
        args=['bash', '-c', command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    proc.kill()
    return Result(
        output=stdout.decode(),
        error=stderr.decode()
    )


def load_dump(dump_name: str = default_dump_name) -> Result:

    """ Загружает дамп в пустую базу, использвать для юнит-тестов """

    db = settings.DATABASES['default']
    command = f'export PGPASSWORD={db["PASSWORD"]};' \
              f'psql -h {db["HOST"]} -p {db["PORT"]} -U {db["USER"]} {db["NAME"]} < {dump_name}'
    proc = subprocess.Popen(
            args=['bash', '-c', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    proc.kill()
    return Result(
        output=stdout.decode(),
        error=stderr.decode()
    )
