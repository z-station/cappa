from typing import Dict, Any

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from app.groups.models import Group, GroupCourse
from app.groups.services import exceptions
from app.tasks.queries import CreateOrUpdateCourseUserStatisticsQuery
from app.tasks.models import UserStatistics, TaskItem          # ← добавили TaskItem
from app.tasks.entities import TaskItemStatistics
from app.tasks.enums import TaskItemType


UserModel = get_user_model()


class GroupStatisticsService:
    """
    Сервис собирает статистику по курсу в группе.

        {
            "tasks_max_points": { получение цены нерешенных задач
                "<task_id_1>": <max_score>,
                "<task_id_2>": <max_score>,
                ...
            },
            "stats": {
                <user_id_1>: {
                    <task_id_1>: {...},
                    ...
                },
                <user_id_2>: {...},
                ...
            }
        }
    """

    @classmethod
    def get_group_course(cls, group: Group, course_id: int) -> GroupCourse:
        try:
            group_course = group.group_courses.get(course_id=course_id)
        except ObjectDoesNotExist:
            raise exceptions.CourseNotFoundException()

        teacher_ok = (
            group.user_is_teacher and group_course.statistics_allow_for_teacher()
        )
        learner_ok = (
            group.user_is_learner and group_course.statistics_allow_for_learner()
        )
        if not teacher_ok and not learner_ok:
            raise exceptions.GroupStatisticPermissionError()

        return group_course

    @classmethod
    def get_course_statistics(
        cls,
        group: Group,
        course_id: int,
    ) -> Dict[str, Any]:
        """
        Возвращает:
            {
                "tasks_max_points": { task_id: max_score, ... },
                "stats":            { user_id:  { task_id: {...}, ... }, ... }
            }
        """

        # собираем stats #
        group_course = cls.get_group_course(group=group, course_id=course_id)
        version_hash = group_course.course.get_cache_data()["version_hash"]
        user_ids: set[int] = set(group.learners.only_ids())

        stats: Dict[int, Dict[int, TaskItemStatistics]] = {}
        objs = UserStatistics.objects.filter(
            type_id=course_id,
            type=TaskItemType.COURSE,
            user_id__in=user_ids,
        )

        for obj in objs:
            if obj.version_hash != version_hash:
                query = CreateOrUpdateCourseUserStatisticsQuery(
                    user_id=obj.user_id,
                    course_id=course_id,
                    version_hash=version_hash,
                )
                obj = UserStatistics.objects.raw(*query.get_sql())[0]

            user_ids.remove(obj.user_id)
            stats[obj.user_id] = obj.data

        for user_id in user_ids:
            query = CreateOrUpdateCourseUserStatisticsQuery(
                user_id=user_id,
                course_id=course_id,
                version_hash=version_hash,
            )
            obj = UserStatistics.objects.raw(*query.get_sql())[0]
            stats[obj.user_id] = obj.data

        # max_score всех задач #
        tasks_qs = TaskItem.objects.filter(
            topic__course=group_course.course
        ).values("id", "max_score")

        tasks_max_points: Dict[str, float] = {
            str(t["id"]): float(t["max_score"]) for t in tasks_qs
        }

        # итоговый ответ API #
        return {
            "tasks_max_points": tasks_max_points,  # ← новое поле
            "stats": stats,                        # прежняя статистика
        }