from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class JavaService(BaseTaskItemService):

    translator_type = TranslatorType.JAVA
