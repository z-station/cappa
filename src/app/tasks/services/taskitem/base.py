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
from app.translators.enums import TranslatorType
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

        if taskitem.task.enabled_tests and taskitem.score_method_with_tests:
            testing_result = cls.testing(
                taskitem=taskitem,
                code=code,
                only_visible=False
            )
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
        for number, test in enumerate(task_tests):
            task_tests[number]['id'] = number
        return task_tests

    @classmethod
    def testing(
        cls,
        taskitem: TaskItem,
        code: str,
        only_visible: bool = True
    ) -> TestingResult:

        """ Testing only enabled task tests,
            return only enabled and visible tests """

        if taskitem.score_method not in ScoreMethod.TESTS_METHODS:
            raise exceptions.OperationNotAllowed()
        testing_checker = taskitem.task.testing_checker
        if not testing_checker:
            raise exceptions.TestingCheckerNotExist()

        service_cls = cls._get_service_cls()
        all_tests = cls._get_tests(taskitem)
        enabled_tests = [el for el in all_tests if el['enabled']]

        # Run enabled tests only
        request_tests = [
            {'data_in': el['data_in'], 'data_out': el['data_out']}
            for el in enabled_tests
        ]
        testing_result = service_cls.testing(
            code=code,
            checker_code=testing_checker.content,
            tests=request_tests
        )
        # Remove hidden tests from result
        result = []
        for test, test_result in zip(enabled_tests, testing_result['tests']):
            test_result['id'] = test['id']
            if only_visible:
                if test['visible']:
                    result.append(test_result)
            else:
                result.append(test_result)
        return {
            'ok': testing_result['ok'],
            'tests': result
        }
