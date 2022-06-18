from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class JavaViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.JAVA
