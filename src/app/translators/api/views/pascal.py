from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class PascalViewSet(BaseViewSet):

    translator_type = TranslatorType.PASCAL
