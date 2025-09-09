from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Rust186ViewSet(BaseViewSet):

    translator_type = TranslatorType.RUST186
