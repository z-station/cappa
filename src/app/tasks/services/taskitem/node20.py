from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class Node20Service(BaseTaskItemService):

    translator_type = TranslatorType.NODE20
