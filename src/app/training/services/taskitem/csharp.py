from app.training.services import BaseTaskItemService
from app.translators.enums import TranslatorType


class CsharpService(BaseTaskItemService):

    translator_type = TranslatorType.CSHARP
