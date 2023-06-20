from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class GCC74Service(BaseTaskItemService):

    translator_type = TranslatorType.GCC74
