from rest_framework.serializers import (
    Serializer,
    CharField,
    ChoiceField,
)
from app.translators.enums import TranslatorType


class DraftSerializer(Serializer):

    content = CharField(required=True)
    translator = ChoiceField(
        required=True,
        choices=TranslatorType.CHOICES
    )
