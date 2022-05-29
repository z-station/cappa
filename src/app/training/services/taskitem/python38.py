from app.training.services import BaseTaskItemService
from app.translators.enums import TranslatorType


class Python38Service(BaseTaskItemService):

    translator_type = TranslatorType.PYTHON38
