from typing import List
from django.contrib.auth import get_user_model
from django.conf import settings
from app.tasks.models import Solution
from app.tasks.enums import SolutionType
from app.training.entities import PlagCheckResult, PlagCheckUser
from app.training.models import TaskItem
from app.translators.enums import TranslatorType
from app.common.services.exceptions import (
    ServiceConnectionError,
    ServiceBadRequest,
)
from app.common.services.mixins import RequestMixin
from app.training.services.exceptions import CheckPlagException

UserModel = get_user_model()


class PlagStatisticsService(RequestMixin):

    langs_map = {
        TranslatorType.PYTHON38: 'python',
        TranslatorType.GCC74: 'cpp',
        TranslatorType.JAVA: 'java',
    }

    @classmethod
    def check_by_taskitem(
        cls,
        taskitem: TaskItem,
        reference_user_id: int,
        candidate_ids: List[int]
    ) -> PlagCheckResult:

        """ TODO prototype """

        course_id = taskitem.topic.course_id
        ref_solution = Solution.objects.filter(
            user_id=reference_user_id,
            type=SolutionType.COURSE,
            type_id=course_id,
            translator=taskitem.translator,
            task_id=taskitem.task_id
        ).first()
        ref_code = ref_solution.content if ref_solution else None
        result = PlagCheckResult(percent=0, candidate=None, reference=None)
        if ref_code:
            candidates_solutions = Solution.objects.filter(
                user_id__in=candidate_ids,
                type=SolutionType.COURSE,
                type_id=course_id,
                translator=taskitem.translator,
                task_id=taskitem.task_id
            ).exclude(
                user_id=reference_user_id
            ).order_by('-created', 'user_id').distinct('created', 'user_id')
            candidates_data = []
            candidates_map = {}
            for solution in candidates_solutions:
                candidates_data.append({
                    "uuid": str(solution.user_id),
                    "code": solution.content
                })
                candidates_map[solution.user_id] = solution.id

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
                data = response.json()
                if data['uuid']:
                    user_id = int(data['uuid'])
                    result = PlagCheckResult(
                        percent=data['percent'],
                        reference=PlagCheckUser(
                            id=reference_user_id,
                            solution_id=ref_solution.id
                        ),
                        candidate=PlagCheckUser(
                            id=user_id,
                            solution_id=candidates_map[user_id]
                        )
                    )
        return result
