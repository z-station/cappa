from app.training.services import BaseTaskItemService
from app.translators.enums import TranslatorType


class PhpService(BaseTaskItemService):

    translator_type = TranslatorType.PHP
