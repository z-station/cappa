from typing import Optional
from django.db import connection, connections


class RawSqlExecutor:

    @staticmethod
    def execute(
        query: str,
        params: Optional[dict] = None
    ):
        with connection.cursor() as cursor:
            cursor.execute(query, params)

    @staticmethod
    def fetchone(
        query: str,
        params: Optional[dict] = None
    ):
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ][0]

    @staticmethod
    def fetch(
        query: str,
        params: Optional[dict] = None,
        stream: bool = False,
        fetch_size: int = 300,
        db: str = 'default'
    ):
        with connections[db].cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            if stream:
                while True:
                    results = cursor.fetchmany(fetch_size)
                    if not results:
                        break
                    for row in results:
                        yield dict(zip(columns, row))
            for row in cursor.fetchall():
                yield dict(zip(columns, row))
