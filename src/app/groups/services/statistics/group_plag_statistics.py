from typing import Dict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from app.groups.services import exceptions
from app.groups.models import Group
from app.tasks.models import UserPlagStatistics
from app.tasks.entities import PlagCheckResult
from app.tasks.enums import TaskItemType


UserModel = get_user_model()


class GroupPlagStatisticsService:

    @classmethod
    def validate_group_course(cls, group: Group, course_id: int):
        try:
            group.group_courses.get(course_id=course_id)
        except ObjectDoesNotExist:
            raise exceptions.CourseNotFoundException()
        else:
            if not group.user_is_teacher:
                raise exceptions.GroupStatisticPermissionError()

    @classmethod
    def get_course_statistics(
        cls,
        group: Group,
        course_id: int,
    ) -> Dict[int, Dict[int, PlagCheckResult]]:

        """ Формат ответа:
            {
                user_id_1: {
                    taskitem_id_1: {
                       percent: float,
                       datetime: str,
                       reference: ?{
                           id: int,
                           solution_type: str,
                           solution_id: int
                       },
                       candidate: ?{
                           id: int,
                           solution_type: str,
                           solution_id: int
                       }
                    },
                    taskitem_id_2: {...},
                    ...
                    taskitem_id_N: {...}
                },
                user_id_2: {...},
                ...
                user_id_N: {...}
            } """

        cls.validate_group_course(group=group, course_id=course_id)
        result = {}
        user_ids = set(group.learners.only_ids())
        objs = UserPlagStatistics.objects.filter(
            type_id=course_id,
            type=TaskItemType.COURSE,
            user_id__in=user_ids
        )
        for obj in objs:
            result[obj.user_id] = obj.data
        return result

