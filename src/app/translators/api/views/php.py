from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class PhpViewSet(BaseViewSet):

    translator_type = TranslatorType.PHP
