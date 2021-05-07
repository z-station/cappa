from tinymce.models import HTMLField

from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DateTimeField,
    PositiveIntegerField,
    TextField
)
from django.contrib.auth import get_user_model
from app.tasks.consts import SolutionSource, Status
from app.tasks.models import Task

UserModel = get_user_model()


class Solution(Model):

    class Meta:
        verbose_name = "решение задачи"
        verbose_name_plural = "решения задач"
        ordering = ('-last_modified',)

    source = CharField(choices=SolutionSource.choices, max_length=50)
    user = ForeignKey(
        UserModel, verbose_name="пользователь",
        related_name='solutions'
    )
    task = ForeignKey(Task, verbose_name="задача", related_name='solutions')
    status = CharField(
        verbose_name='статус решения', max_length=2,
        choices=Status.choices
    )
    created = DateTimeField(verbose_name='дата создания', auto_now_add=True)
    last_modified = DateTimeField(
        verbose_name="дата последнего изменения",
        auto_now_add=True
    )
    count_tests = PositiveIntegerField(
        verbose_name='кол-во тестов на момент решения'
    )
    count_passed_tests = PositiveIntegerField(
        verbose_name='кол-во пройденных тестов',
    )
    content = TextField(
        verbose_name="листинг решения",
        blank=True, default=''
    )
    reviewer = ForeignKey(
        UserModel, verbose_name='рецензент',
        related_name='reviewed_solutions',
        blank = True, null = True
    )
    reviewer_comment = HTMLField(
        verbose_name="комментарий рецензента",
        blank=True, null=True
    )

    @property
    def status_name(self) -> str:
        return Status.names[self.status]

    def _set_status(self):

        if self.count_passed_tests == 0:
            self.status = Status.UN_LUCK
        elif self.count_passed_tests == self.count_tests:
            self.status = Status.SUCCESS
        else:
            self.status = Status.IN_PROGRESS

    def save(self, *args, **kwargs):
        self._set_status()
        super().save(*args, **kwargs)
