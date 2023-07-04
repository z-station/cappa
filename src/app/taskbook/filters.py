from django_filters import (
    FilterSet,
    RangeFilter,
    MultipleChoiceFilter
)
from app.tasks.models.taskitem import TaskItem
from app.tasks.enums import DifficultyLevel
from app.tasks.filters import TagsFilter
from app.common.widgets import (
    CheckboxMultiple,
)


class TaskBookFilter(FilterSet):

    class Meta:
        model = TaskItem
        fields = []

    rating = RangeFilter(
        label='Рейтинг',
        required=False,
        field_name='task__rating'
    )

    difficulty = MultipleChoiceFilter(
        label='Сложность',
        choices=DifficultyLevel.CHOICES,
        widget=CheckboxMultiple(),
        required=False,
        field_name='task__difficulty',
        lookup_expr='icontains'
    )

    tags = TagsFilter(
        label='Метки',
        null_label='Без меток',
        widget=CheckboxMultiple(),
        required=False,
        field_name='task__tags',
    )
