from abc import abstractmethod
from typing import Type
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from app.tasks.models.taskitem import TaskItem
from app.tasks import services
from app.common.services.exceptions import ServiceException
from app.common.api.serializers import BadRequestSerializer
from app.translators.enums import TranslatorType
from app.tasks.api.serializers.taskitem import (
    CreateSolutionSerializer,
    TestingSerializer,
)


class BaseTaskItemViewSet(GenericViewSet):

    queryset = TaskItem.objects.show()
    serializer_class = None
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'create_solution':
            return self.queryset.prefetch_related('topic__course')
        else:
            return self.queryset

    @abstractmethod
    def translator_type(self) -> TranslatorType:
        pass

    @classmethod
    def _get_service_cls(cls) -> Type[services.BaseTaskItemService]:
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
        elif cls.translator_type == TranslatorType.RUST186:
            return services.Rust186Service

    def get_serializer_class(self):
        if self.action == 'create_solution':
            return CreateSolutionSerializer
        elif self.action == 'testing':
            return TestingSerializer

    @action(methods=('POST',), detail=True, url_path='create-solution')
    def create_solution(self, request, *args, **kwargs):
        taskitem = self.get_object()
        slz = self.get_serializer(data=request.data)
        slz.is_valid(raise_exception=True)
        service_cls = self._get_service_cls()
        try:
            solution = service_cls.create_solution(
                taskitem=taskitem,
                user=request.user,
                **slz.validated_data
            )
        except ServiceException as ex:
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
            return Response({'solution_id': solution.id})

    @action(methods=('POST',), detail=True)
    def testing(self, request, *args, **kwargs):
        taskitem = self.get_object()
        slz = self.get_serializer(data=request.data)
        slz.is_valid(raise_exception=True)
        service_cls = self._get_service_cls()
        try:
            data = service_cls.testing(
                taskitem=taskitem,
                **slz.validated_data
            )
        except ServiceException as ex:
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
            slz = self.get_serializer(instance=data)
            return Response(slz.data)
