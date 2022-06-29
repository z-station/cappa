from django.shortcuts import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from app.groups.models import Group
from app.groups.api.serializers import GroupStatisticsSerializer
from app.groups.services import (
    GroupStatisticsService,
    GroupPlagStatisticsService
)
from app.groups.services import exceptions


class GroupViewSet(GenericViewSet):

    queryset = Group.objects.all()
    serializer_class = None
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action in ('statistics', 'plag_statistics'):
            return GroupStatisticsSerializer

    def get_permissions(self):
        if self.action in ('statistics', 'plag_statistics'):
            return (IsAuthenticated(),)
        else:
            return (AllowAny(),)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'statistics':
            queryset = Group.objects.with_user_is_learner(
                self.request.user
            ).with_user_is_teacher(
                self.request.user
            ).prefetch_related('members', 'courses')
        elif self.action == 'plag_statistics':
            queryset = Group.objects.with_user_is_teacher(
                self.request.user
            ).prefetch_related('members', 'courses')
        return queryset

    @action(methods=('GET',), detail=True)
    def statistics(self, request, *args, **kwargs):
        group = self.get_object()
        slz = self.get_serializer(data=request.GET)
        slz.is_valid(raise_exception=True)
        try:
            data = GroupStatisticsService.get_course_statistics(
                group=group,
                course_id=slz.data['course_id'],
            )
        except exceptions.CourseNotFoundException:
            raise Http404
        except exceptions.GroupStatisticPermissionError:
            raise PermissionDenied
        return Response(data)

    @action(methods=('GET',), detail=True, url_path='plag-statistics')
    def plag_statistics(self, request, *args, **kwargs):
        group = self.get_object()
        slz = self.get_serializer(data=request.GET)
        slz.is_valid(raise_exception=True)
        try:
            data = GroupPlagStatisticsService.get_course_statistics(
                group=group,
                course_id=slz.data['course_id'],
            )
        except exceptions.CourseNotFoundException:
            raise Http404
        except exceptions.GroupStatisticPermissionError:
            raise PermissionDenied
        return Response(data)
