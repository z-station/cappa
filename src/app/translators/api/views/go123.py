from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Go123ViewSet(BaseViewSet):

    translator_type = TranslatorType.GO123
