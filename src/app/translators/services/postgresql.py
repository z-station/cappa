from typing import List
from django.conf import settings
from app.translators.enums import TranslatorType
from app.translators.services.base import BaseTranslatorService
from app.common.services import exceptions
from app.translators.services.entities import (
    Test,
    DebugResult,
    TestingResult
)
from rest_framework.serializers import ValidationError
from app.translators.services.serializers import (
    PostgresqlResponseDebugSerializer,
    PostgresqlResponseTestingSerializer
)


class PostgresqlService(BaseTranslatorService):

    SERVICE_HOST = settings.SERVICES_HOSTS[TranslatorType.POSTGRESQL]

    @classmethod
    def debug(
        cls,
        code: str,
        **kwargs
    ) -> DebugResult:

        name: str = kwargs.get('name')
        response = cls._perform_request(
            url=f'{cls.SERVICE_HOST}/debug/',
            data={
                'format': 'tabular',
                'code': code,
                'name': name
            }
        )

        slz = PostgresqlResponseDebugSerializer(data=response.json())
        try:
            slz.is_valid(raise_exception=True)
        except ValidationError as ex:
            raise exceptions.ServiceInvalidResponse(
                details={'error': str(ex)}
            )
        return slz.validated_data

    @classmethod
    def testing(
        cls,
        code: str,
        tests: List[Test],
        **kwargs
    ) -> TestingResult:

        response = cls._perform_request(
            url=f'{cls.SERVICE_HOST}/testing/',
            data={
                'code': code,
                'name': kwargs['name'],
                'request_type': kwargs['request_type'],
                'tests': [
                    {'data_in': test['data_in'] for test in tests}
                ]
            }
        )
        slz = PostgresqlResponseTestingSerializer(data=response.json())
        try:
            slz.is_valid(raise_exception=True)
        except ValidationError as ex:
            raise exceptions.ServiceInvalidResponse(
                details={'error': str(ex)}
            )
        return slz.validated_data
