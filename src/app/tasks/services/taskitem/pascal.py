from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class PascalService(BaseTaskItemService):

    translator_type = TranslatorType.PASCAL
