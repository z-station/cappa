from rest_framework.serializers import (
    Serializer,
    CharField,
    BooleanField
)


class ResponseDebugSerializer(Serializer):

    result = CharField(required=True, allow_null=True)
    error = CharField(required=True, allow_null=True)


class ResponseTestSerializer(Serializer):

    ok = BooleanField(required=True)
    result = CharField(required=True, allow_null=True)
    error = CharField(required=True, allow_null=True)


class ResponseTestingSerializer(Serializer):

    ok = BooleanField(required=True)
    tests = ResponseTestSerializer(many=True)
