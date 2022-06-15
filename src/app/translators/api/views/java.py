from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class JavaViewSet(BaseViewSet):

    translator_type = TranslatorType.JAVA
