from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class CsharpService(BaseTaskItemService):

    translator_type = TranslatorType.CSHARP
