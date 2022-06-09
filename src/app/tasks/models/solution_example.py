from django.db import models
from django.contrib.auth import get_user_model
from app.translators.enums import TranslatorType
from app.tasks.models import Task

UserModel = get_user_model()


class SolutionExample(models.Model):

    class Meta:
        verbose_name = "эталонное решение"
        verbose_name_plural = "эталонные решения"

    translator = models.CharField(
        verbose_name='транслятор кода',
        choices=TranslatorType.CHOICES,
        max_length=100
    )
    content = models.TextField(
        verbose_name='текст решения',
        blank=True,
        null=True
    )
    task = models.ForeignKey(Task, related_name='solution_examples')

    def __str__(self):
        return ''
