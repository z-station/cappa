import os
from django.conf import settings


def get_db_file_path(instance, filename):
    name = filename.split('.')[0]
    filename = f'{name}.sql'
    return os.path.join(settings.SQL_FILES_DIR, filename)
