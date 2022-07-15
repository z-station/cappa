from typing import List
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from app.tasks.models import Solution
from app.tasks.enums import SolutionType
from app.training.entities import (
    PlagCheckResult,
    PlagCheckUser
)
from app.training.models import (
    TaskItem,
    CourseUserPlagStatistics
)
from app.translators.enums import TranslatorType
from app.common.services.exceptions import (
    ServiceConnectionError,
    ServiceBadRequest,
)
from app.common.services.mixins import RequestMixin
from app.training.services.exceptions import (
    CheckPlagImpossible,
    CheckPlagException,
    SolutionNotFound,
)
from app.training.api.serializers.statisitics import (
    PlagCheckResultSerializer
)

UserModel = get_user_model()


class PlagStatisticsService(RequestMixin):

    langs_map = {
        TranslatorType.PYTHON38: 'python',
        TranslatorType.GCC74: 'cpp',
        TranslatorType.JAVA: 'java',
    }

    @classmethod
    def _get_candidates_solutions(
        cls,
        reference_user_id: int,
        taskitem: TaskItem,
        candidate_ids: List[int],
    ):
        course_id = taskitem.topic.course_id
        return Solution.objects.filter(
            user_id__in=candidate_ids,
            type=SolutionType.COURSE,
            type_id=course_id,
            translator=taskitem.translator,
            task_id=taskitem.task_id
        ).exclude(
            user_id=reference_user_id
        ).order_by(
            '-created',
            'user_id'
        ).distinct(
            'created',
            'user_id'
        )

    @classmethod
    def _get_external_solutions(
        cls,
        taskitem: TaskItem,
    ):
        return Solution.objects.filter(
            type=SolutionType.EXTERNAL,
            translator=taskitem.translator,
            task_id=taskitem.task_id
        ).order_by(
            '-created',
            'external_source_id'
        ).distinct(
            'created',
            'external_source_id'
        )

    @classmethod
    def _get_reference_solution(
        cls,
        taskitem: TaskItem,
        reference_user_id: int,
    ):
        return Solution.objects.filter(
            user_id=reference_user_id,
            type=SolutionType.COURSE,
            type_id=taskitem.topic.course_id,
            translator=taskitem.translator,
            task_id=taskitem.task_id
        ).first()

    @classmethod
    def _get_solution_uuid(cls, solution: Solution) -> str:
        if solution.type == SolutionType.EXTERNAL:
            user_id = solution.external_source_id
        else:
            user_id = solution.user_id
        return f'{solution.type}-{user_id}-{solution.id}'

    @classmethod
    def _get_candidates_data(
        cls,
        taskitem: TaskItem,
        reference_user_id: int,
        candidate_ids: List[int]
    ) -> list:

        candidates_solutions = cls._get_candidates_solutions(
            reference_user_id=reference_user_id,
            taskitem=taskitem,
            candidate_ids=candidate_ids
        )
        external_solutions = cls._get_external_solutions(
            taskitem=taskitem,
        )
        all_solutions = candidates_solutions.union(external_solutions)
        candidates_data = []
        for solution in all_solutions:
            candidates_data.append({
                "uuid": cls._get_solution_uuid(solution),
                "code": solution.content
            })
        return candidates_data

    @classmethod
    def _get_plag_data(
        cls,
        taskitem: TaskItem,
        ref_code: str,
        candidates_data: list
    ):
        try:
            response = cls._perform_request(
                url=f'{settings.ANTIPLAG_HOST}/check/',
                data={
                    "lang": cls.langs_map[taskitem.translator],
                    "ref_code": ref_code,
                    "candidates": candidates_data
                },
                timeout=10
            )
        except (ServiceConnectionError, ServiceBadRequest) as ex:
            raise CheckPlagException(details=ex.details)
        else:
            return response.json()

    @classmethod
    def create_or_update_taskitem_statistics(
        cls,
        user_id: int,
        taskitem: TaskItem,
        data: PlagCheckResult
    ):
        serialized_data = PlagCheckResultSerializer(instance=data).data
        statistics, created = CourseUserPlagStatistics.objects.get_or_create(
            user_id=user_id,
            course_id=taskitem.topic.course_id,
            defaults={'data': {taskitem.id: serialized_data}}
        )
        if not created:
            statistics.data[taskitem.id] = serialized_data
            statistics.save()

    @classmethod
    def check_by_taskitem(
        cls,
        taskitem: TaskItem,
        reference_user_id: int,
        candidate_ids: List[int]
    ) -> PlagCheckResult:

        """ TODO prototype """

        ref_solution = cls._get_reference_solution(
            reference_user_id=reference_user_id,
            taskitem=taskitem,
        )
        if not ref_solution or not ref_solution.content:
            raise SolutionNotFound()

        result = PlagCheckResult(
            percent=0,
            datetime=timezone.now(),
            reference=PlagCheckUser(
                id=reference_user_id,
                solution_type=SolutionType.COURSE,
                solution_id=ref_solution.id
            ),
            candidate=None
        )
        candidates_data = cls._get_candidates_data(
            taskitem=taskitem,
            reference_user_id=reference_user_id,
            candidate_ids=candidate_ids
        )
        if candidates_data:
            plag_data = cls._get_plag_data(
                taskitem=taskitem,
                ref_code=ref_solution.content,
                candidates_data=candidates_data
            )
            percent = plag_data['percent']
            if percent == -1:
                raise CheckPlagImpossible()
            solution_type, user_id, solution_id = (
                plag_data['uuid'].split('-')
            )
            result['percent'] = percent
            result['candidate'] = PlagCheckUser(
                id=user_id,
                solution_type=solution_type,
                solution_id=solution_id
            )
        cls.create_or_update_taskitem_statistics(
            user_id=reference_user_id,
            taskitem=taskitem,
            data=result
        )
        return result
