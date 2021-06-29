import os
from typing import Tuple
from django.core.management import BaseCommand
from django.conf import settings
from datetime import datetime


class Command(BaseCommand):

    help = """ 
        Выгрузить базу данных в файл
    
        Файл будет сохранен в директорию: backup/<дата>/<время>-<метка>.sql
        Пригоден для запуска только внутри контейнера,
        т.к. работает контейнерной базой
        
        Пример №1 выгрузка 
        python manage.py backup_db
        --------------------------------------------
        Пример №2 выгрузка с указанием метки файла 
        python manage.py backup_db -t some-tag        
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-t', '--tag', type=str, dest='tag',
            help='метка, будет добавлена к названию файла'
        )

    def _get_filepath(self, **kwargs) -> Tuple[str, str]:
        str_date = datetime.now().strftime('%Y-%m-%d')
        str_time = datetime.now().strftime('%H-%M-%S')
        backup_dir = os.path.join(settings.BASE_DIR, 'backup')
        tag = kwargs.get('tag')
        if tag:
            filename = f'{str_date}-{str_time}-{tag}.sql'
        else:
            filename = f'{str_date}-{str_time}.sql'
        file_dir = f'{backup_dir}/{str_date}'
        file_path = f'{file_dir}/{filename}'
        return file_dir, file_path

    def handle(self, *args, **options):
        file_dir, file_path = self._get_filepath(**options)
        db_user = settings.DATABASES['default']['USER']
        db_name = settings.DATABASES['default']['NAME']
        db_host = settings.DATABASES['default']['HOST']
        db_pass = settings.DATABASES['default']['PASSWORD']
        command = f'mkdir -p {file_dir} && ' \
                  f'export PGPASSWORD={db_pass} && ' \
                  f'pg_dump -U {db_user} -h {db_host} {db_name} > {file_path}'
        os.system(command)
        self.stdout.write(self.style.SUCCESS(f'file: {file_path}'))