import os
from typing import Union
from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):

    help = """
        Загрузить базу данных Postgres из файла
        Пригоден для запуска только внутри контейнера, 
        т.к. работает контейнерной базой.
        
        Пример №1 Целевой файл в директории backup/2020-11-20/2020-11-20-[00:00:00].sql
        python manage.py restore_db -f 2020-11-20-[00:00:00].sql
        ---------------------------------------------------------
        Пример №2 Целевой файл в корне backup/pg.dump
        python manage.py restore_db -f pg.dump
        ---------------------------------------------------------    
        Пример №3 Последний созданный файл 
        python manage.py restore_db 
    """

    backup_dir = '/app/backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--file', type=str, dest='filename',
            help='указать имя файла'
        )

    def _get_newest_file_from_dir(self, path: str) -> Union[str, None]:
        result = None
        for filename in reversed(os.listdir(path)):
            filepath = f'{path}/{filename}'
            if os.path.isfile(filepath):
                result = filepath
        return result

    def _get_newest_filepath(self) -> Union[str, None]:
        filepath = None
        for dirname in reversed(os.listdir(self.backup_dir)):
            path = f'{self.backup_dir}/{dirname}'
            if os.path.isdir(path):
                filepath = self._get_newest_file_from_dir(path)
                if filepath:
                    break
        return filepath

    def _get_filepath(self, **kwargs) -> str:
        filename = kwargs.get('filename')
        if filename:
            dirname_end_index = filename.find('[')
            if dirname_end_index > 0:
                dirname = filename[:dirname_end_index]
                filepath = f'{self.backup_dir}/{dirname}/{filename}'
            else:
                filepath = f'{self.backup_dir}/{filename}'
        else:
            filepath = self._get_newest_filepath()
        return filepath

    def handle(self, *args, **options):
        filepath = self._get_filepath(**options)
        if filepath:
            db_user = settings.DATABASES['default']['USER']
            db_name = settings.DATABASES['default']['NAME']
            db_host = settings.DATABASES['default']['HOST']
            db_pass = settings.DATABASES['default']['PASSWORD']
            command = f'export PGPASSWORD={db_pass} && ' \
                      f'dropdb -f --if-exists -U {db_user} -h {db_host} {db_name} && ' \
                      f'createdb -U {db_user} -h {db_host} {db_name} && ' \
                      f'psql -U {db_user} -h {db_host} {db_name} < {filepath} &&' \
                      f'python manage.py migrate'
            os.system(command)
            self.stdout.write(self.style.SUCCESS(f'restored file: {filepath}'))
        else:
            self.stdout.write(self.style.WARNING(f'file path not found: {filepath}'))
