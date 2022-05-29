from datetime import datetime
from typing import Optional
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.tasks.models import (
    Solution,
    Task,
    Source
)
from app.tasks.enums import (
    ReviewStatus,
    SolutionType,
    ScoreMethod
)
from app.translators.enums import TranslatorType
from app.tasks import exceptions


UserModel = get_user_model()


class SolutionService:

    @classmethod
    def create_course_solution(
        cls,
        course_id: int,
        course_name: str,
        user: UserModel,
        max_score: int,
        task: Task,
        content: str,
        translator: TranslatorType,
        score_method: ScoreMethod,
        count_tests: Optional[int] = None,
        count_passed_tests: Optional[int] = None,
        testing_score: Optional[float] = None,
        due_date: Optional[datetime] = None
    ) -> Solution:

        if Solution.objects.by_user(user.id).by_task(
            task.id
        ).by_course(course_id).count() > 20:
            raise exceptions.SolutionsLimit()
        solution = Solution(
            type=SolutionType.COURSE,
            type_id=course_id,
            type_name=course_name,
            user=user,
            user_first_name=user.first_name,
            user_last_name=user.last_name,
            user_father_name=user.father_name,
            user_email=user.email,
            user_username=user.username,
            max_score=max_score,
            task=task,
            task_name=task.title,
            content=content,
            translator=translator,
            testing_score=testing_score,
            count_tests=count_tests,
            count_passed_tests=count_passed_tests,
            score_method=score_method,
            due_date=due_date
        )
        if score_method in ScoreMethod.REVIEW_METHODS:
            solution.review_status = ReviewStatus.READY_TO_REVIEW
        solution.save()
        return solution

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
        solution.reviewer = reviewer
        solution.reviewer_first_name = reviewer.first_name
        solution.reviewer_last_name = reviewer.last_name
        solution.reviewer_father_name = reviewer.father_name
        solution.hide_review_score = hide_review_score
        solution.hide_reviewer_comment = hide_reviewer_comment
        solution.save()
        return solution

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
            Создание внешнего решения

            Параметры:
            - source - внешний источник решения
            - description - пояснение или ссылка на решение в интернете,
                подтверждающая, что решение является общеизвестным
            - task - задача к которой относится решение
            - content - программный код решения
            - translator - язык программирования, на котором написан код """

        return Solution.objects.create(
            type=SolutionType.EXTERNAL,
            description=description,
            external_source=external_source,
            external_source_name=external_source.name,
            task=task,
            task_name=task.title,
            content=content,
            translator=translator,
        )
