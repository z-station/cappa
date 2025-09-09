from app.tasks.services.taskitem.base import BaseTaskItemService
from app.translators.enums import TranslatorType


class Rust186Service(BaseTaskItemService):

    translator_type = TranslatorType.RUST186
