from app.tasks.models import TaskItem


class TaskBookItem(TaskItem):

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        proxy = True
