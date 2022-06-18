from app.training.api.views import BaseTaskItemViewSet
from app.translators.enums import TranslatorType


class PostgresqlViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.POSTGRESQL
