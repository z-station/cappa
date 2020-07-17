from django.db import models
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from src.utils.consts import langs, tasks

UserModel = get_user_model()


class Source(models.Model):

    class Meta:
        verbose_name = "источник"
        verbose_name_plural = "источники"
        ordering = ('name',)

    name = models.CharField(verbose_name="имя", max_length=255)
    description = models.TextField(verbose_name="описание", blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):

    class Meta:
        verbose_name = "метка"
        verbose_name_plural = "метки"
        ordering = ('name',)

    name = models.CharField(verbose_name="имя", max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
        ordering = ('order_key',)

    INT = 'int'
    FLOAT = 'float'
    STR = 'str'
    OUTPUT_TYPES = (
        (STR, 'строка'),
        (INT, 'целое число'),
        (FLOAT, 'вещественное число')
    )

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=0)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    show = models.BooleanField(verbose_name="отображать", default=False)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    content = HTMLField(verbose_name="текст задания", default="", blank=True, null=True)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    output_type = models.CharField(
        verbose_name='чекер', max_length=255,
        choices=OUTPUT_TYPES, default=STR
    )
    difficulty = models.CharField(
        verbose_name='сложность', choices=tasks.CHOICES,
        max_length=255, blank=True, null=True
    )
    source = models.ForeignKey(Source, verbose_name='источник', blank=True, null=True, on_delete=models.SET_NULL)
    lang = models.CharField(
        verbose_name='язык', choices=langs.CHOICES,
        blank=True, null=True, max_length=255
    )
    tags = models.ManyToManyField(Tag, verbose_name='метки', related_name='tasks', blank=True)
    tests = JSONField(verbose_name='автотесты', default=list, blank=True, null=True)

    def __str__(self):
        return self.title


class SolutionExample(models.Model):

    class Meta:
        verbose_name = "эталонное решение"
        verbose_name_plural = "эталонные решения"

    lang = models.CharField(
        verbose_name='язык', choices=langs.CHOICES,
        max_length=255, blank=True, null=True
    )
    content = models.TextField(verbose_name='код рещения', blank=True, null=True)
    task = models.ForeignKey(Task, related_name='solution_examples')

    def __str__(self):
        return ''
