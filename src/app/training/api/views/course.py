from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from app.training.models import Course
from app.tasks.services.statistics import UserStatisticsService


class CourseViewSet(GenericViewSet):

    queryset = Course.objects.all()
    serializer_class = None
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'statistics':
            return (IsAuthenticated(),)
        else:
            return (AllowAny(),)

    @action(methods=('GET',), detail=True)
    def statistics(self, request, *args, **kwargs):
        course = self.get_object()
        data = UserStatisticsService.get_course_statistics(
            user_id=request.user.id,
            course_id=course.id,
            version_hash=course.get_cache_data()['version_hash']
        )
        return Response(data)
