from django_filters import (
    FilterSet,
    NumberFilter,
    MultipleChoiceFilter,
)
from app.tasks.models import Solution, Tag
from app.common.filters import DefaultOrderingFilter


class SolutionsFilterSet(FilterSet):

    class Meta:
        model = Solution
        fields = (
            'task_id',
        )

    task_id = NumberFilter()
    order = DefaultOrderingFilter(
        default=('-created',),
        fields=(
            ('created', 'created'),
        )
    )


class TagsFilter(MultipleChoiceFilter):

    @property
    def field(self):
        qs = Tag.objects.exclude(
            tasks=True
        ).order_by('name')
        choices = [(elem.id, elem.name) for elem in qs]
        self.extra['choices'] = choices
        return super().field
