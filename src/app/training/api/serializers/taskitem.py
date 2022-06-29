from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    BooleanField
)
from app.training.models.taskitem import TaskItem


class TestSerializer(Serializer):

    ok = BooleanField(read_only=True)
    result = CharField(read_only=True)
    error = CharField(read_only=True)


class TestingSerializer(Serializer):

    code = CharField(write_only=True)
    ok = BooleanField(read_only=True)
    tests = TestSerializer(many=True, read_only=True)


class CreateSolutionSerializer(Serializer):

    code = CharField(write_only=True)


class TaskItemSerializer(ModelSerializer):

    class Meta:
        model = TaskItem
        fields = '__all__'
