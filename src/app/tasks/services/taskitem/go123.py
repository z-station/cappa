from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class Go123Service(BaseTaskItemService):

    translator_type = TranslatorType.GO123
