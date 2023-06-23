import django_filters
from django import forms
from app.tasks.models.taskitem import TaskItem
from app.tasks.enums import DifficultyLevel


class TaskBookFilter(django_filters.FilterSet):

    class Meta:
        model = TaskItem
        fields = []  # TODO проверить что это выражение корректно

    rating = django_filters.RangeFilter(
        label='Рейтинг',
        required=False,
        field_name='task__rating'
    )

    difficulty = django_filters.MultipleChoiceFilter(
        label='Сложность',
        choices=DifficultyLevel.CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        field_name='task__difficulty',
        lookup_expr='icontains'
    )

    TAGS_CHOICES = [
        ('conditions', 'Условия'),
        ('cycles', 'Циклы'),
    ]
    # TODO можно ли легально переопределить AllValueMultipleFilter
    tags = django_filters.AllValuesMultipleFilter(
        label='Метки',
        null_label='Без меток',
        # choices=TAGS_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        field_name='task__tags',
        # lookup_expr='icontains'
    )

