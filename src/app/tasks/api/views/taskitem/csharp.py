from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class CSharpViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.CSHARP
