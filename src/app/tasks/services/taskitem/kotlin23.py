from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class Kotlin23Service(BaseTaskItemService):

    translator_type = TranslatorType.KOTLIN23
