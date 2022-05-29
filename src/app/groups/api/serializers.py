from rest_framework.serializers import (
    Serializer,
    IntegerField
)


class GroupStatisticsSerializer(Serializer):

    course_id = IntegerField(min_value=1, required=True)
