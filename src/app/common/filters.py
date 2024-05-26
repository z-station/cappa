from typing import Tuple, Optional
from django_filters.rest_framework import (
    OrderingFilter
)


class DefaultOrderingFilter(OrderingFilter):

    def __init__(
        self,
        *args,
        default: Optional[Tuple[str]] = None,
        **kwargs
    ):
        self.default = default
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        value = value or self.default
        return super().filter(qs, value)
