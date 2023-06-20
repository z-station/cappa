from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet
from app.translators.enums import TranslatorType


class PostgresqlViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.POSTGRESQL
