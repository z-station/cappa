from rest_framework.serializers import (
    Serializer,
    CharField,
)


class BaseDebugSerializer(Serializer):

    code = CharField(write_only=True, required=True)
    result = CharField(read_only=True, allow_null=True)
    error = CharField(read_only=True, allow_null=True)

    def validate_data_in(self, value):
        return value if value else None


class DebugSerializer(BaseDebugSerializer):

    data_in = CharField(
        write_only=True,
        required=False,
        allow_null=True,
        allow_blank=True
    )


class PostgresqlDebugSerializer(BaseDebugSerializer):

    name = CharField(
        write_only=True,
        required=True,
    )
