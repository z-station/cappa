from app.training.services import BaseTaskItemService
from app.translators.enums import TranslatorType


class GCC74Service(BaseTaskItemService):

    translator_type = TranslatorType.GCC74
