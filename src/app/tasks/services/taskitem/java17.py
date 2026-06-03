from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class Java17Service(BaseTaskItemService):

    translator_type = TranslatorType.JAVA17
