from rest_framework.serializers import (
    Serializer,
    CharField,
    BooleanField,
    ListField,
)
from app.common.api.fields import AnyField


class PostgresqlResponseDebugSerializer(Serializer):

    result = CharField(required=True, allow_null=True, allow_blank=True)
    error = CharField(required=True, allow_null=True, allow_blank=True)


class PostgresqlResponseTestSerializer(Serializer):

    ok = BooleanField(required=True)
    error = CharField(required=True, allow_null=True, allow_blank=True)


class PostgresqlResponseTestingSerializer(Serializer):

    ok = BooleanField(required=True)
    tests = PostgresqlResponseTestSerializer(many=True)
