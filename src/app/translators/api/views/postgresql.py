from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from app.translators.api.serializers import PostgresqlDebugSerializer
from app.common.api.serializers import BadRequestSerializer
from app.common.services import exceptions
from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class PostgresqlViewSet(BaseViewSet):

    translator_type = TranslatorType.POSTGRESQL

    @action(methods=('POST',), detail=False)
    def debug(self, request, *args, **kwargs):
        slz = PostgresqlDebugSerializer(data=request.data)
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
            slz = PostgresqlDebugSerializer(instance=data)
            return Response(slz.data)
