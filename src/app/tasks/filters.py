from django_filters import (
    FilterSet,
    NumberFilter
)
from app.tasks.models import Solution
from app.common.filters import DefaultOrderingFilter


class SoluionsFilterSet(FilterSet):

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
