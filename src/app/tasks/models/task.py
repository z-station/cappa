from django.db import models
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from app.translators.enums import CheckerType
from app.tasks.enums import DifficultyLevel
from app.tasks.models import (
    Tag,
    Source
)


UserModel = get_user_model()


class Task(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    order_key = models.PositiveIntegerField(
        verbose_name='порядок',
        default=0
    )
    last_modified = models.DateTimeField(
        verbose_name="дата последнего изменения",
        auto_now=True
    )
    show = models.BooleanField(
        verbose_name="отображать",
        default=False
    )
    title = models.CharField(
        verbose_name="заголовок",
        max_length=255
    )
    content = HTMLField(
        verbose_name="текст задания",
        default="",
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        UserModel,
        verbose_name="автор",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    output_type = models.CharField(
        verbose_name='чекер',
        max_length=255,
        choices=CheckerType.CHOICES,
        default=CheckerType.STR
    )
    difficulty = models.CharField(
        verbose_name='сложность',
        choices=DifficultyLevel.CHOICES,
        max_length=255,
        blank=True,
        null=True
    )
    rating = models.PositiveIntegerField(
        default=0,
        verbose_name='рейтинг',
        help_text='рассчитывается автоматически'
    )
    source = models.ForeignKey(
        Source,
        verbose_name='источник',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='метки',
        related_name='tasks',
        blank=True
    )
    tests = JSONField(
        verbose_name='автотесты',
        default=list,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
