from typing import Dict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from app.groups.models import Group, GroupCourse
from app.groups.services import exceptions
from app.training.queries import CreateOrUpdateCourseUserStatisticsQuery
from app.training.models import CourseUserStatistics
from app.training.entities import TaskItemStatistics


UserModel = get_user_model()


class GroupStatisticsService:

    @classmethod
    def get_group_course(cls, group: Group, course_id: int) -> GroupCourse:
        try:
            group_course = group.group_courses.get(
                course_id=course_id
            )
        except ObjectDoesNotExist:
            raise exceptions.CourseNotFoundException()
        else:
            teacher_permission = (
                group.user_is_teacher and group_course.statistics_allow_for_teacher()
            )
            learner_permission = (
                group.user_is_learner and group_course.statistics_allow_for_learner()
            )
            if not teacher_permission and not learner_permission:
                raise exceptions.GroupStatisticPermissionError()
            return group_course

    @classmethod
    def get_course_statistics(
        cls,
        group: Group,
        course_id: int,
    ) -> Dict[int, Dict[int, TaskItemStatistics]]:

        """ Формат ответа:
            {
                user_id_1: {
                    taskitem_id_1: {...},
                    taskitem_id_2: {...},
                    ...
                    taskitem_id_N: {...}
                },
                user_id_2: {...},
                ...
                user_id_N: {...}
            } """

        result = {}
        group_course = cls.get_group_course(
            group=group,
            course_id=course_id
        )
        version_hash = group_course.course.get_cache_data()['version_hash']
        user_ids = set(group.learners.only_ids())

        objs = list(
            CourseUserStatistics.objects.filter(
                course_id=course_id,
                user_id__in=user_ids
            )
        )
        for obj in objs:
            if obj.version_hash != version_hash:
                query = CreateOrUpdateCourseUserStatisticsQuery(
                    user_id=obj.user_id,
                    course_id=course_id,
                    version_hash=version_hash,
                )
                obj = CourseUserStatistics.objects.raw(*query.get_sql())[0]
            user_ids.remove(obj.user_id)
            result[obj.user_id] = obj.data

        # users without statistics
        for user_id in user_ids:
            query = CreateOrUpdateCourseUserStatisticsQuery(
                user_id=user_id,
                course_id=course_id,
                version_hash=version_hash,
            )
            obj = CourseUserStatistics.objects.raw(*query.get_sql())[0]
            result[obj.user_id] = obj.data
        return result
