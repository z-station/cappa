from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from app.common.api.permissions import TeacherPermission
from app.tasks.api.serializers.statisitics import (
    CheckPlagSerializer
)
from app.tasks.services.statistics import PlagStatisticsService
from app.tasks.models.taskitem import TaskItem
from app.tasks.services.exceptions import (
    CheckPlagException,
    SolutionNotFound,
    CheckPlagImpossible,
)


class TaskItemViewSet(GenericViewSet):

    queryset = TaskItem.objects.all()
    serializer_class = None
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'check_plag':
            return (TeacherPermission(),)
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'check_plag':
            slz = CheckPlagSerializer
        else:
            slz = super().get_serializer_class()
        return slz

    @action(methods=('POST',), detail=True, url_path='check-plag')
    def check_plag(self, request, *args, **kwargs):
        taskitem = self.get_object()
        slz = self.get_serializer(data=request.data)
        slz.is_valid(raise_exception=True)
        try:
            data = PlagStatisticsService.check_by_taskitem(
                taskitem=taskitem,
                reference_user_id=slz.validated_data['reference_user_id'],
                candidate_ids=slz.validated_data['candidates'],
                translator=taskitem.translator[0]
            )
        except (CheckPlagException, CheckPlagImpossible) as ex:
            return Response(data=ex.as_dict(), status=500)
        except SolutionNotFound:
            return Response(data={}, status=204)
        else:
            return Response(data=data, status=200)
