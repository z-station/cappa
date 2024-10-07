from typing import Optional
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.tasks.models import (
    Solution,
    Task,
    Source,
    TaskItem,
)
from app.tasks.enums import (
    ReviewStatus,
    TaskItemType,
    ScoreMethod
)
from app.translators.enums import TranslatorType
from app.tasks import exceptions
from app.translators.services.entities import (
    TestingResult,
)


UserModel = get_user_model()


class SolutionService:

    @classmethod
    def create_internal(
        cls,
        taskitem: TaskItem,
        user: UserModel,
        content: str,
        translator: TranslatorType,
        testing_result: Optional[TestingResult] = None
    ) -> Solution:

        """ Создание решения по курсу

            Параметры:
            - taskitem - задача
            - user - автор решения
            - task - задача к которой относится решение
            - content - программный код решения
            - translator - язык программирования, на котором написан код
            - testing_result - результаты прохождения тестов

            review_score не передается т.к. оценка преподавателя выставляется
                после создания решения """

        if Solution.objects.by_user(user.id).by_task(
            taskitem.task.id
        ).by_type(taskitem.type).count() > 20:
            raise exceptions.SolutionsLimit()

        if (
            taskitem.score_method in ScoreMethod.TESTS_METHODS
            and testing_result
        ):
            count_tests = len(taskitem.task.enabled_tests)
            count_passed_tests = 0
            for test in testing_result['tests']:
                if test['ok']:
                    count_passed_tests += 1
            testing_score = round(
                count_passed_tests / count_tests * taskitem.max_score, 2
            )
        else:
            count_tests = count_passed_tests = testing_score = None

        score = testing_score if taskitem.score_method_is_tests else None

        data = {
            'type': taskitem.type,
            'user': user,
            'user_first_name': user.first_name,
            'user_last_name': user.last_name,
            'user_father_name': user.father_name,
            'user_email': user.email,
            'user_username': user.username,
            'max_score': taskitem.max_score,
            'task': taskitem.task,
            'task_name': taskitem.task.title,
            'content': content,
            'translator': translator,
            'testing_score': testing_score,
            'count_tests': count_tests,
            'count_passed_tests': count_passed_tests,
            'score_method': taskitem.score_method,
            'score': score,
        }
        if taskitem.type == TaskItemType.COURSE:
            data['type_id'] = taskitem.topic.course_id
            data['type_name'] = taskitem.topic.course.title
            data['due_date'] = taskitem.topic.due_date
        if taskitem.score_method in ScoreMethod.REVIEW_METHODS:
            data['review_status'] = ReviewStatus.READY_TO_REVIEW
        return Solution.objects.create(**data)

    @classmethod
    def create_external(
        cls,
        external_source: Source,
        description: str,
        task: Task,
        content: str,
        translator: TranslatorType,
    ) -> Solution:

        """
            Создание внешнего решения.

            Внешнее решение это решения существующие в иных источниках,
            откуда студенты могут списать, нужны чтобы видеть плагиатные
            решения

            Параметры:
            - source - внешний источник решения
            - description - пояснение или ссылка на решение в интернете,
                подтверждающая, что решение является общеизвестным
            - task - задача к которой относится решение
            - content - программный код решения
            - translator - язык программирования, на котором написан код """

        return Solution.objects.create(
            type=TaskItemType.EXTERNAL,
            description=description,
            external_source=external_source,
            external_source_name=external_source.name,
            task=task,
            task_name=task.title,
            content=content,
            translator=translator,
        )

    @classmethod
    def review(
        cls,
        reviewer: UserModel,
        solution: Solution,
        review_status: Optional[ReviewStatus],
        review_score: Optional[float] = None,
        reviewer_comment: Optional[float] = None,
        hide_review_score: float = False,
        hide_reviewer_comment: float = False
    ):

        """ Изменение статуса ручной проверки решения преподавателем

            reviewer - пользователь, преподаватель
            solution - решение на проверке
            review_status - статус проверки
            review_score - оценка преподавателя
            reviewer_comment - комментарий преподавателя к решению
            hide_review_score - скрыть оценку от ученика
            hide_reviewer_comment - скрыть комментарий от ученика """

        if review_score is not None:
            if review_score < 0 or review_score > solution.max_score:
                raise exceptions.InvalidScoreValue()
        if review_status == ReviewStatus.CHECKED and review_score is None:
            raise exceptions.ScoreRequired()
        if solution.score_method not in ScoreMethod.REVIEW_METHODS:
            raise exceptions.ReviewUnAvailable()

        solution.review_status = review_status
        if review_score:
            solution.review_score = review_score
        if reviewer_comment is not None:
            solution.reviewer_comment = reviewer_comment
        if review_score and review_status == ReviewStatus.CHECKED:
            solution.review_date = timezone.now()
            solution.score = review_score
        else:
            solution.review_date = None
            solution.score = None
        solution.reviewer = reviewer
        solution.reviewer_first_name = reviewer.first_name
        solution.reviewer_last_name = reviewer.last_name
        solution.reviewer_father_name = reviewer.father_name
        solution.hide_review_score = hide_review_score
        solution.hide_reviewer_comment = hide_reviewer_comment
        solution.save()
        return solution
