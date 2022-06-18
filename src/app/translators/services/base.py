from typing import List
from app.common.services import exceptions
from app.common.services.mixins import RequestMixin
from app.translators.services.entities import (
    Test,
    DebugResult,
    TestingResult
)
from rest_framework.serializers import ValidationError
from app.translators.services.serializers import (
    ResponseDebugSerializer,
    ResponseTestingSerializer
)


class BaseTranslatorService(RequestMixin):

    SERVICE_HOST = None

    @classmethod
    def debug(
        cls,
        code: str,
        **kwargs
    ) -> DebugResult:

        response = cls._perform_request(
            url=f'{cls.SERVICE_HOST}/debug/',
            data={
                'data_in': kwargs.get('data_in'),
                'code': code,
            }
        )
        slz = ResponseDebugSerializer(data=response.json())
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
                'checker': kwargs['checker_code'],
                'tests': tests
            }
        )
        slz = ResponseTestingSerializer(data=response.json())
        try:
            slz.is_valid(raise_exception=True)
        except ValidationError as ex:
            raise exceptions.ServiceInvalidResponse(
                details={'error': str(ex)}
            )
        return slz.validated_data
