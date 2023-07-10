from django_filters import (
    FilterSet,
    RangeFilter,
    MultipleChoiceFilter,
    CharFilter
)
from django.forms.widgets import (
    TextInput
)
from app.tasks.models.taskitem import TaskItem
from app.tasks.enums import DifficultyLevel
from app.translators.enums import TranslatorType
from app.tasks.filters import TagsFilter
from app.common.widgets import (
    CheckboxMultiple,
)


class TaskBookFilter(FilterSet):

    class Meta:
        model = TaskItem
        fields = []

    search = CharFilter(
        label='Поиск',
        field_name='task__title',
        lookup_expr='icontains',
        widget=TextInput(
            attrs={
                'placeholder': 'Поиск по названию',
                'type': 'search',
                'class': 'form-control'
            }
        )
    )

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

    lang = MultipleChoiceFilter(
        label='Язык',
        choices=TranslatorType.CHOICES,
        widget=CheckboxMultiple(),
        required=False,
        field_name='translator',
        lookup_expr='icontains'
    )
