from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class PrologDViewSet(BaseViewSet):

    translator_type = TranslatorType.PROLOG_D
