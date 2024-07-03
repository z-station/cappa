from django.contrib.auth import get_user_model
from app.tasks.services import exceptions
from app.tasks.services.taskitem.base import BaseTaskItemService
from app.tasks.models import TaskItem
from app.translators.services.entities import TestingResult
from app.translators.enums import TranslatorType
from app.tasks.enums import ScoreMethod

UserModel = get_user_model()


class PostgresqlService(BaseTaskItemService):

    translator_type = TranslatorType.POSTGRESQL

    @classmethod
    def testing(
        cls,
        taskitem: TaskItem,
        code: str,
        only_visible: bool = True
    ) -> TestingResult:

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
            name=taskitem.get_db_name(),
            request_type=testing_checker.content,
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
