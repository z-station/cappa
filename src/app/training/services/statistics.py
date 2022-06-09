from typing import Optional, Dict
from django.contrib.auth import get_user_model
from app.common.raw_sql.executor import RawSqlExecutor
from app.training.queries import (
    CreateOrUpdateUserTaskItemStatisticQuery,
    CreateOrUpdateCourseUserStatisticsQuery,
    UpdateCourseUserStatisticsQuery
)
from app.training.models import CourseUserStatistics
from app.training.entities import TaskItemStatistics


UserModel = get_user_model()


class UserStatisticsService:

    @classmethod
    def create_or_update_taskitem_statistics(
        cls,
        user_id: int,
        course_id: int,
        version_hash: str,
        taskitem_id: Optional[int] = None
    ):

        """ Пересчитывает статистику решения задачи
            для пользователя """

        query = CreateOrUpdateUserTaskItemStatisticQuery(
            user_id=user_id,
            course_id=course_id,
            version_hash=version_hash,
            taskitem_id=taskitem_id
        )
        RawSqlExecutor.execute(*query.get_sql())

    @classmethod
    def create_or_update_course_statistics(
        cls,
        user_id: int,
        course_id: int,
        version_hash: str,
    ):

        """ Пересчитывает статистику решения задач курса
            для указанного пользователя """

        query = CreateOrUpdateCourseUserStatisticsQuery(
            user_id=user_id,
            course_id=course_id,
            version_hash=version_hash,
        )
        RawSqlExecutor.execute(*query.get_sql())

    @classmethod
    def update_course_statistics(
        cls,
        user_id: int,
        course_id: int,
    ):
        """ Используется чтобы обновить статистику
            если решение было изменено в процессе проведения ревью

            Вызывается обновление всей статистики по курсу вместо обновления
            статстики по конкретной taskitem_id
            т.к. оно не известно при ревью """

        query = UpdateCourseUserStatisticsQuery(
            user_id=user_id,
            course_id=course_id,
        )
        RawSqlExecutor.execute(*query.get_sql())

    @classmethod
    def get_course_statistics(
        cls,
        user_id: int,
        course_id: int,
        version_hash: str,
    ) -> Dict[int, TaskItemStatistics]:

        """ Формат ответа:
            {
                taskitem_id_1: {...},
                taskitem_id_2: {...},
                ...
                taskitem_id_N: {...}
            } """

        obj = CourseUserStatistics.objects.filter(
            course_id=course_id,
            user_id=user_id
        ).first()
        if obj is None or obj.version_hash != version_hash:
            query = CreateOrUpdateCourseUserStatisticsQuery(
                user_id=user_id,
                course_id=course_id,
                version_hash=version_hash,
            )
            obj = CourseUserStatistics.objects.raw(*query.get_sql())
            obj = obj[0]
        return obj.data
