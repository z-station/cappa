from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class Ruby4Service(BaseTaskItemService):

    translator_type = TranslatorType.RUBY4
