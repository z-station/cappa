from rest_framework.serializers import (
    Serializer,
    IntegerField,
    ListField,
    FloatField,
    DateTimeField,
    ChoiceField,
)
from app.tasks.enums import TaskItemType


class CheckPlagSerializer(Serializer):

    reference_user_id = IntegerField(required=True)
    candidates = ListField(required=True, child=IntegerField())


class PlagCheckUserSerializer(Serializer):

    id = IntegerField(required=True)
    solution_id = IntegerField(required=True)
    solution_type = ChoiceField(
        required=True,
        choices=TaskItemType.CHOICES
    )


class PlagCheckResultSerializer(Serializer):

    percent = FloatField(required=True)
    datetime = DateTimeField(required=True)
    reference = PlagCheckUserSerializer(required=True)
    candidate = PlagCheckUserSerializer(allow_null=True)
