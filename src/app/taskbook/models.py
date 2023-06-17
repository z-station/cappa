from typing import Optional
from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from app.tasks.models import Task
from app.tasks.enums import ScoreMethod
from app.translators.enums import TranslatorType
from app.common.fields import TaskItemSlugField
from app.databases.models import Database


class TaskBookItem(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ['id']

    show = models.BooleanField(
        verbose_name="отображать",
        default=True
    )
    task = models.ForeignKey(
        Task,
        verbose_name='задача',
        related_name='taskbook_items'
    )
    max_score = models.PositiveIntegerField(
        verbose_name='балл за решение',
        default=5
    )
    score_method = models.CharField(
        verbose_name='метод оценивания',
        max_length=50,
        choices=ScoreMethod.CHOICES,
        default=ScoreMethod.TESTS
    )
    slug = TaskItemSlugField(
        verbose_name="слаг",
        max_length=255,
        blank=True,
        null=True,
    )
    translator = ArrayField(
        verbose_name='транслятор кода',
        base_field=models.CharField(
            choices=TranslatorType.CHOICES,
            max_length=100
        ),
    )
    database = models.ForeignKey(
        Database,
        verbose_name='учебная база данных',
        help_text='обязательна для задач по базам данных',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    @property
    def title(self):
        return self.task.title

    def get_absolute_url(self):
        return reverse('taskbook:taskitem', kwargs={'taskitem': self.slug})

    def get_db_name(self) -> Optional[str]:
        return self.database.db_name if self.database else None

    def score_method_is_tests(self):
        return self.score_method == ScoreMethod.TESTS

    def score_method_is_review(self):
        return self.score_method == ScoreMethod.REVIEW

    def score_method_is_tests_and_review(self):
        return self.score_method == ScoreMethod.TESTS_AND_REVIEW

    def __str__(self):
        return self.title
