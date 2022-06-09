from rest_framework.serializers import (
    Serializer,
    CharField,
    DictField
)


class BadRequestSerializer(Serializer):

    message = CharField(required=True)
    details = DictField(required=True, allow_empty=True)
