import os
from django.conf import settings
from app.databases.models import Database
from app.databases.enums import DatabaseStatus
from app.common.services.mixins import RequestMixin
from app.common.services import exceptions
from app.translators.enums import TranslatorType


class DatabaseManagementService(RequestMixin):

    SERVICE_HOST = settings.SERVICES_HOSTS[TranslatorType.POSTGRESQL]

    @classmethod
    def create(cls, obj: Database):
        filename = os.path.basename(obj.file.name)
        cls._perform_request(
            url=f'{cls.SERVICE_HOST}/create/',
            data={
                'name': obj.db_name,
                'filename': filename
            }
        )

    @classmethod
    def delete(cls, obj: Database):
        cls._perform_request(
            url=f'{cls.SERVICE_HOST}/delete/{obj.db_name}/',
            data={}
        )

    @classmethod
    def status(cls, obj: Database) -> DatabaseStatus:
        response = cls._perform_request(
            url=f'{cls.SERVICE_HOST}/status/{obj.db_name}/',
            method='get',
            data={}
        )
        data = response.json()
        return data['status']
