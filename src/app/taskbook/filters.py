import django_filters
from django import forms

from app.taskbook.models import TaskBookItem


class TaskBookFilter(django_filters.FilterSet):
    rating = django_filters.RangeFilter(label="Рейтинг",
                                        required=False)

    DIFFICULT_CHOICES = [
        ('easy', 'Легкая'),
        ('normal', 'Нормальная'),
        ('hard', 'Сложная'),
        ('legendary', 'Легендарная'),
    ]
    difficulty = django_filters.MultipleChoiceFilter(label='Сложность',
                                                     choices=DIFFICULT_CHOICES,
                                                     widget=forms.CheckboxSelectMultiple(),
                                                     required=False)

    TAGS_CHOICES = [
        ('conditions', 'Условия'),
        ('cycles', 'Циклы'),
    ]
    tags = django_filters.MultipleChoiceFilter(label='Метки',
                                               choices=TAGS_CHOICES,
                                               widget=forms.CheckboxSelectMultiple(),
                                               required=False)

    class Meta:
        model = TaskBookItem
        fields = []


qs = TaskBookItem.objects.filter(show=True)

f = TaskBookFilter({'rating_min': 0, 'rating_max': 100}, queryset=qs)
