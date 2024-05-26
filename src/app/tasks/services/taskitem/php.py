from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class PhpService(BaseTaskItemService):

    translator_type = TranslatorType.PHP
