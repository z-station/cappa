from app.training.services import BaseTaskItemService
from app.translators.enums import TranslatorType


class PrologDService(BaseTaskItemService):

    translator_type = TranslatorType.PROLOG_D
