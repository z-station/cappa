from django.contrib.auth import get_user_model
from app.training.services import exceptions
from app.training.services import BaseTaskItemService
from app.training.models import TaskItem
from app.translators.services.entities import TestingResult
from app.translators.enums import TranslatorType, CheckerType
from app.tasks.enums import ScoreMethod

UserModel = get_user_model()


class PostgresqlService(BaseTaskItemService):

    translator_type = TranslatorType.POSTGRESQL

    @classmethod
    def testing(
        cls,
        taskitem: TaskItem,
        code: str,
    ) -> TestingResult:

        if taskitem.score_method not in ScoreMethod.TESTS_METHODS:
            raise exceptions.OperationNotAllowed()
        request_type = CheckerType.MAP[taskitem.task.output_type]
        service_cls = cls._get_service_cls()
        return service_cls.testing(
            code=code,
            name=taskitem.get_db_name(),
            request_type=request_type,
            tests=cls._get_tests(taskitem)
        )
