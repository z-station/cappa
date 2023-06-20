from typing import List, Type
from django.contrib.auth import get_user_model
from app.tasks.services import exceptions
from app.tasks.services.statistics import UserStatisticsService
from app.translators.services.entities import (
    Test,
)
from app.tasks.models import TaskItem
from app.translators.services.entities import (
    TestingResult,
)
from app.translators import services
from app.translators.enums import TranslatorType, CheckerType
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
        elif cls.translator_type == TranslatorType.POSTGRESQL:
            return services.PostgresqlService
        elif cls.translator_type == TranslatorType.PASCAL:
            return services.PascalService
        elif cls.translator_type == TranslatorType.PHP:
            return services.PhpService
        elif cls.translator_type == TranslatorType.CSHARP:
            return services.CsharpService
        elif cls.translator_type == TranslatorType.JAVA:
            return services.JavaService

    @classmethod
    def create_solution(
        cls,
        taskitem: TaskItem,
        user: UserModel,
        code: str
    ) -> Solution:

        if taskitem.task.tests and taskitem.score_method_with_tests():
            testing_result = cls.testing(taskitem=taskitem, code=code)
        else:
            testing_result = None
        solution = SolutionService.create_internal(
            taskitem=taskitem,
            user=user,
            content=code,
            translator=cls.translator_type,
            testing_result=testing_result
        )
        if taskitem.type_course:
            version_hash = taskitem.topic.course.get_cache_data()['version_hash']
            UserStatisticsService.create_or_update_taskitem_statistics(
                user_id=user.id,
                course_id=taskitem.topic.course_id,
                version_hash=version_hash,
                taskitem_id=taskitem.id
            )
        return solution

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
    def testing(
        cls,
        taskitem: TaskItem,
        code: str,
    ) -> TestingResult:

        if taskitem.score_method not in ScoreMethod.TESTS_METHODS:
            raise exceptions.OperationNotAllowed()
        checker_code = CheckerType.MAP[taskitem.task.output_type]
        service_cls = cls._get_service_cls()
        return service_cls.testing(
            code=code,
            checker_code=checker_code,
            tests=cls._get_tests(taskitem)
        )
