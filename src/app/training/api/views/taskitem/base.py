from abc import abstractmethod
from typing import Type
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from app.training.models import (
    TaskItem,
)
from app.training import services
from app.common.services.exceptions import ServiceException
from app.common.api.serializers import BadRequestSerializer
from app.translators.enums import TranslatorType
from app.training.api.serializers.taskitem import (
    CreateSolutionSerializer,
    TestingSerializer,
)
from app.training.services import UserStatisticsService


class BaseTaskItemViewSet(GenericViewSet):

    queryset = TaskItem.objects.all()
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
            course = taskitem.topic.course
            UserStatisticsService.create_or_update_taskitem_statistics(
                user_id=request.user.id,
                course_id=course.id,
                version_hash=course.get_cache_data()['version_hash'],
                taskitem_id=taskitem.id
            )
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
