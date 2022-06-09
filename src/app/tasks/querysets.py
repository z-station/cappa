from django.db.models import QuerySet
from app.tasks.enums import SolutionType


class SolutionQueryset(QuerySet):

    def external(self):
        return self.filter(type=SolutionType.EXTERNAL)

    def internal(self):
        return self.exclude(type=SolutionType.EXTERNAL)

    def type_course(self):
        return self.filter(type=SolutionType.COURSE)

    def by_course(self, course_id: int):
        return self.filter(
            type=SolutionType.COURSE,
            type_id=course_id
        )

    def by_user(self, user_id: int):
        return self.filter(
            user_id=user_id
        )

    def by_task(self, task_id: int):
        return self.filter(
            task_id=task_id
        )
