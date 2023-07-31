from typing import List
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from app.tasks.models import Solution
from app.tasks.enums import TaskItemType
from app.tasks.entities import (
    PlagCheckResult,
    PlagCheckUser,
    CandidateData,
    PlagData,
)
from app.tasks.models import (
    TaskItem,
    UserPlagStatistics
)
from app.translators.enums import TranslatorType
from app.common.services.exceptions import (
    ServiceConnectionError,
    ServiceBadRequest,
)
from app.common.services.mixins import RequestMixin
from app.tasks.services.exceptions import (
    CheckPlagImpossible,
    CheckPlagException,
    SolutionNotFound,
)
from app.tasks.api.serializers.statisitics import (
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
        translator: TranslatorType.LITERALS
    ):
        course_id = taskitem.topic.course_id
        return Solution.objects.filter(
            user_id__in=candidate_ids,
            type=TaskItemType.COURSE,
            type_id=course_id,
            translator=translator,
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
        translator: TranslatorType.LITERALS
    ):
        return Solution.objects.filter(
            type=TaskItemType.EXTERNAL,
            translator=translator,
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
        translator: TranslatorType.LITERALS
    ):
        return Solution.objects.filter(
            user_id=reference_user_id,
            type=TaskItemType.COURSE,
            type_id=taskitem.topic.course_id,
            translator=translator,
            task_id=taskitem.task_id
        ).first()

    @classmethod
    def _get_solution_uuid(cls, solution: Solution) -> str:
        if solution.type == TaskItemType.EXTERNAL:
            user_id = solution.external_source_id
        else:
            user_id = solution.user_id
        return f'{solution.type}-{user_id}-{solution.id}'

    @classmethod
    def _get_candidates_data(
        cls,
        taskitem: TaskItem,
        reference_user_id: int,
        candidate_ids: List[int],
        translator: TranslatorType.LITERALS
    ) -> List[CandidateData]:

        candidates_solutions = cls._get_candidates_solutions(
            reference_user_id=reference_user_id,
            taskitem=taskitem,
            candidate_ids=candidate_ids,
            translator=translator
        )
        external_solutions = cls._get_external_solutions(
            taskitem=taskitem,
            translator=translator
        )
        all_solutions = candidates_solutions.union(external_solutions)
        candidates_data = []
        for solution in all_solutions:
            candidates_data.append(
                CandidateData(
                    uuid=cls._get_solution_uuid(solution),
                    code=solution.content
                )
            )
        return candidates_data

    @classmethod
    def _get_plag_data(
        cls,
        ref_code: str,
        candidates_data: List[CandidateData],
        translator: TranslatorType.LITERALS
    ) -> PlagData:
        print(f'{settings.ANTIPLAG_HOST}/check/')
        try:
            response = cls._perform_request(
                url=f'{settings.ANTIPLAG_HOST}/check/',
                data={
                    "lang": cls.langs_map[translator],
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
        statistics, created = UserPlagStatistics.objects.get_or_create(
            user_id=user_id,
            type_id=taskitem.topic.course_id,
            type=TaskItemType.COURSE,
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
        candidate_ids: List[int],
        translator: TranslatorType.LITERALS
    ) -> PlagCheckResult:

        """
            Вычисляет и сохраняет значение плагиата по задаче для пользователя

            Формат ответа:
            {
                "percent": float,
                "datetime": str,
                "reference": {
                    "id": int,             // user id
                    "solution_type": str,  // course | external | taskbook
                    "solution_id": int     // checked solution id
                },
                "candidate": {
                    "id": int,
                    "solution_type": str,
                    "solution_id": int
                }
            }

        """

        ref_solution = cls._get_reference_solution(
            reference_user_id=reference_user_id,
            taskitem=taskitem,
            translator=translator
        )
        if not ref_solution or not ref_solution.content:
            raise SolutionNotFound()

        result = PlagCheckResult(
            percent=0,
            datetime=timezone.now(),
            reference=PlagCheckUser(
                id=reference_user_id,
                solution_type=TaskItemType.COURSE,
                solution_id=ref_solution.id
            ),
            candidate=None
        )
        candidates_data = cls._get_candidates_data(
            taskitem=taskitem,
            reference_user_id=reference_user_id,
            candidate_ids=candidate_ids,
            translator=translator,
        )
        if candidates_data:
            plag_data = cls._get_plag_data(
                ref_code=ref_solution.content,
                candidates_data=candidates_data,
                translator=translator
            )
            percent = plag_data['percent']
            if percent == -1:
                raise CheckPlagImpossible()
            solution_type, user_id, solution_id = (
                plag_data['uuid'].split('-')
            )
            result['percent'] = percent
            result['candidate'] = PlagCheckUser(
                id=int(user_id),
                solution_type=solution_type,
                solution_id=int(solution_id)
            )
        cls.create_or_update_taskitem_statistics(
            user_id=reference_user_id,
            taskitem=taskitem,
            data=result
        )
        return result
