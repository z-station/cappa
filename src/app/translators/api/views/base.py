from abc import abstractmethod
from typing import Type
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from app.translators.api.serializers import DebugSerializer
from app.common.api.serializers import BadRequestSerializer
from app.translators import services
from app.common.services import exceptions
from app.translators.enums import TranslatorType


class BaseViewSet(ViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    @abstractmethod
    def translator_type(self) -> TranslatorType:
        pass

    @classmethod
    def _get_service_cls(cls) -> Type[services.BaseTranslatorService]:
        if cls.translator_type == TranslatorType.PYTHON38:
            return services.Python38Service
        elif cls.translator_type == TranslatorType.GCC74:
            return services.GCC74Service
        elif cls.translator_type == TranslatorType.PROLOG_D:
            return services.PrologDService
        elif cls.translator_type == TranslatorType.POSTGRESQL:
            return services.PostgresqlService
        elif cls.translator_type == TranslatorType.PASCAL:
            return services.PascalService
        elif cls.translator_type == TranslatorType.PHP:
            return services.PhpService
        elif cls.translator_type == TranslatorType.CSHARP:
            return services.CsharpService
        elif cls.translator_type == TranslatorType.JAVA:
            return services.JavaService

    @action(methods=('POST',), detail=False)
    def debug(self, request, *args, **kwargs):
        slz = DebugSerializer(data=request.data)
        slz.is_valid(raise_exception=True)
        service_cls = self._get_service_cls()
        try:
            data = service_cls.debug(**slz.validated_data)
        except exceptions.ServiceException as ex:
            slz = BadRequestSerializer(
                data={
                    'message': ex.message,
                    'details': ex.details
                }
            )
            slz.is_valid(raise_exception=True)
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=slz.validated_data
            )
        else:
            slz = DebugSerializer(instance=data)
            return Response(slz.data)
