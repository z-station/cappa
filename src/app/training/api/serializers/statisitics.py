from rest_framework.serializers import (
    Serializer,
    IntegerField,
    ListField,
)


class CheckPlagSerializer(Serializer):

    reference_user_id = IntegerField(required=True)
    candidates = ListField(required=True, child=IntegerField())
