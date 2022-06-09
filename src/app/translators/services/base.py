import requests
from typing import Optional, List
from app.translators import exceptions
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


class BaseTranslatorService:

    SERVICE_HOST = None

    @classmethod
    def _perform_request(
        cls,
        url: str,
        data: dict
    ) -> requests.Response:

        try:
            response = requests.post(url=url, json=data)
        except Exception as e:
            raise exceptions.ServiceConnectionError(
                details={
                    'error': str(e)
                }
            )
        else:
            if not response.ok:
                raise exceptions.ServiceBadRequest(
                    details={
                        'code': response.status_code,
                        'error': response.json()
                    }
                )
        return response

    @classmethod
    def debug(
        cls,
        code: str,
        data_in: Optional[str] = None
    ) -> DebugResult:

        response = cls._perform_request(
            url=f'{cls.SERVICE_HOST}/debug/',
            data={
                'data_in': data_in,
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
        checker_code: str,
        tests: List[Test]
    ) -> TestingResult:

        response = cls._perform_request(
            url=f'{cls.SERVICE_HOST}/testing/',
            data={
                'code': code,
                'checker': checker_code,
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
