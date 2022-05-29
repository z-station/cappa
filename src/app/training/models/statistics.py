from django.db.models import (
    Model,
    ForeignKey,
    CharField,
)
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from app.training.models import Course

UserModel = get_user_model()


class CourseUserStatistics(Model):

    """ Данные статистики пользователя по курсу

        Формат хранения данных статистики пользователя по задачам курса:
        data = {
            taskitem_id_1: {          // данные последнего решения по задаче курса
                id: int,              // id последнего решения пользователя по задаче курса
                created: str,         // utc дата создания решения
                translator: str,      // id транслятора ЯП
                score_method: str,    // id оценочного метода
                max_score: str        // максимальный балл за решение
                review_score: int|null,  // оценка преподавателя (для ручного метода проверки)
                review_status: str|null, // статус проверки решения преподавателем (для ручного метода проверки)
                testing_score: str|null, // оценка по автотестам (для метода провери на основании тестов)
                due_date: str|null,      // дата сдачи решения
            },
            taskitem_id_2 : {...},
            ...,
            taskitem_id_N : {...}
        }
     """

    class Meta:
        unique_together = ('user', 'course')

    version_hash = CharField(max_length=128)
    data = JSONField(default=dict)
    course = ForeignKey(Course)
    user = ForeignKey(UserModel)
