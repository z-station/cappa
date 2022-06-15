from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class CSharpViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.CSHARP
