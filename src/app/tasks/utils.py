from django.db import transaction

from app.common.raw_sql.executor import RawSqlExecutor
from app.tasks.models import Solution
from app.tasks.queries import UpdateRatingQuery


def calculate_rating():
    query = UpdateRatingQuery()
    with transaction.atomic():
        RawSqlExecutor.execute(query.get_sql())
        Solution.objects.filter(
            rating_is_calculated=False
        ).update(
            rating_is_calculated=True
        )
