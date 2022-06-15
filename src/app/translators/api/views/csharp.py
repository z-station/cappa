from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class CSharpViewSet(BaseViewSet):

    translator_type = TranslatorType.CSHARP
