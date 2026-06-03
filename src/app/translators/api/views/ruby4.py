from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Ruby4ViewSet(BaseViewSet):

    translator_type = TranslatorType.RUBY4
