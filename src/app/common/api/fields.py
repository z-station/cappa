from rest_framework.serializers import Field


class AnyField(Field):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value
