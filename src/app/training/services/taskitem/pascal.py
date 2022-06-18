from app.training.services import BaseTaskItemService
from app.translators.enums import TranslatorType


class PascalService(BaseTaskItemService):

    translator_type = TranslatorType.PASCAL
