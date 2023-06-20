from django.db.models import QuerySet
from app.tasks.enums import TaskItemType


class SolutionQueryset(QuerySet):

    def external(self):
        return self.filter(type=TaskItemType.EXTERNAL)

    def internal(self):
        return self.exclude(type=TaskItemType.EXTERNAL)

    def type_taskbook(self):
        return self.filter(type=TaskItemType.TASKBOOK)

    def type_course(self):
        return self.filter(type=TaskItemType.COURSE)

    def by_course(self, course_id: int):
        return self.filter(
            type=TaskItemType.COURSE,
            type_id=course_id
        )

    def by_user(self, user_id: int):
        return self.filter(user_id=user_id)

    def by_task(self, task_id: int):
        return self.filter(task_id=task_id)

    def by_type(self, type: TaskItemType.LITERALS):
        return self.filter(type=type)


class TaskItemQuerySet(QuerySet):

    def show(self):
        return self.filter(show=True)

    def external(self):
        return self.filter(type=TaskItemType.EXTERNAL)

    def internal(self):
        return self.exclude(type=TaskItemType.EXTERNAL)

    def type_taskbook(self):
        return self.filter(type=TaskItemType.TASKBOOK)

    def type_course(self):
        return self.filter(type=TaskItemType.COURSE)
