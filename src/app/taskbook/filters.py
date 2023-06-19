import django_filters
from django import forms

from app.accounts import models
from app.taskbook.models import TaskBookItem
from app.tasks.enums import DifficultyLevel


class TaskBookFilter(django_filters.FilterSet):
    rating = django_filters.RangeFilter(label='Рейтинг',
                                        required=False,
                                        field_name='task__rating')

    difficulty = django_filters.MultipleChoiceFilter(label='Сложность',
                                                     choices=DifficultyLevel.CHOICES,
                                                     widget=forms.CheckboxSelectMultiple(),
                                                     required=False,
                                                     field_name='task__difficulty',
                                                     lookup_expr='icontains')

    TAGS_CHOICES = [
        ('conditions', 'Условия'),
        ('cycles', 'Циклы'),
    ]
    tags = django_filters.MultipleChoiceFilter(label='Метки',
                                               choices=TAGS_CHOICES,
                                               widget=forms.CheckboxSelectMultiple(),
                                               required=False,
                                               field_name='task__tags',
                                               lookup_expr='icontains')

    class Meta:
        model = TaskBookItem
        fields = []
