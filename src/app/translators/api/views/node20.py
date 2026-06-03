from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Node20ViewSet(BaseViewSet):

    translator_type = TranslatorType.NODE20
