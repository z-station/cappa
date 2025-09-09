from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Rust186ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.RUST186
