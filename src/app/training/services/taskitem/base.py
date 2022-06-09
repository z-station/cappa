from typing import List, Type, Optional
from django.contrib.auth import get_user_model
from app.training.services import (
    exceptions,
    UserStatisticsService
)
from app.training.services.taskitem.entities import (
    Test,
    TestingData
)
from app.training.models import TaskItem
from app.translators.services.entities import (
    TestingResult,
)
from app.translators import services
from app.translators.enums import TranslatorType
from app.translators.checkers import CHECKERS
from app.tasks.models import (
    Solution
)
from app.tasks.enums import (
    ScoreMethod,
)
from app.tasks.services import SolutionService

UserModel = get_user_model()


class BaseTaskItemService:

    translator_type = None

    @classmethod
    def _get_service_cls(cls) -> Type[services.BaseTranslatorService]:
        if cls.translator_type == TranslatorType.PYTHON38:
            return services.Python38Service
        elif cls.translator_type == TranslatorType.GCC74:
            return services.GCC74Service
        elif cls.translator_type == TranslatorType.PROLOG_D:
            return services.PrologDService

    @classmethod
    def _get_tests(cls, taskitem: TaskItem) -> List[Test]:
        task_tests = taskitem.task.tests
        if not isinstance(task_tests, list) or len(task_tests) == 0:
            raise exceptions.TestsNotFound()
        return [
            Test(
                data_in=task_test['input'],
                data_out=task_test['output']
            ) for task_test in task_tests
        ]

    @classmethod
    def _get_success_tests_count(cls, testing_result: TestingResult) -> int:
        success_tests_count = 0
        for test in testing_result['tests']:
            if test['ok']:
                success_tests_count += 1
        return success_tests_count

    @classmethod
    def _get_testing_data(
        cls,
        code: str,
        taskitem: TaskItem
    ) -> TestingData:

        if taskitem.score_method in ScoreMethod.TESTS_METHODS:
            count_tests = len(taskitem.task.tests)
            if count_tests:
                testing_result = cls.testing(
                    taskitem=taskitem,
                    code=code
                )
                count_passed_tests = cls._get_success_tests_count(
                    testing_result
                )
                testing_score = round(
                    count_passed_tests / count_tests * taskitem.max_score, 2
                )
            else:
                count_tests = 0
                count_passed_tests = 0
                testing_score = 0
        else:
            count_tests = None
            count_passed_tests = None
            testing_score = None

        return TestingData(
            count_tests=count_tests,
            count_passed_tests=count_passed_tests,
            testing_score=testing_score
        )

    @classmethod
    def create_solution(
        cls,
        taskitem: TaskItem,
        user: UserModel,
        code: str
    ) -> Solution:

        count_tests, count_passed_tests, testing_score = (
            cls._get_testing_data(
                code=code,
                taskitem=taskitem
            )
        )
        solution = SolutionService.create_course_solution(
            user=user,
            course_id=taskitem.topic.course_id,
            course_name=taskitem.topic.course.title,
            max_score=taskitem.max_score,
            task=taskitem.task,
            content=code,
            translator=cls.translator_type,
            count_tests=count_tests,
            count_passed_tests=count_passed_tests,
            testing_score=testing_score,
            score_method=taskitem.score_method,
            due_date=taskitem.topic.due_date,
        )
        version_hash = taskitem.topic.course.get_cache_data()['version_hash']
        UserStatisticsService.create_or_update_taskitem_statistics(
            user_id=user.id,
            course_id=taskitem.topic.course_id,
            version_hash=version_hash,
            taskitem_id=taskitem.id
        )
        return solution

    @classmethod
    def testing(
        cls,
        taskitem: TaskItem,
        code: str,
    ) -> TestingResult:

        if taskitem.score_method not in ScoreMethod.TESTS_METHODS:
            raise exceptions.OperationNotAllowed()
        checker_code = CHECKERS[taskitem.task.output_type]
        service_cls = cls._get_service_cls()
        return service_cls.testing(
            code=code,
            checker_code=checker_code,
            tests=cls._get_tests(taskitem)
        )
