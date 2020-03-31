from django.db import models
from django.contrib.postgres.fields import JSONField
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Source(models.Model):

    class Meta:
        verbose_name = "источник материалов"
        verbose_name_plural = "источники материалов"
        ordering = ('order_key',)

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=0)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    content = HTMLField(verbose_name="содержимое", default="", blank=True, null=True)

    def __str__(self):
        return self.title


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
    show = models.BooleanField(verbose_name="отображать", default=False)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    content = HTMLField(verbose_name="текст задания", default="", blank=True, null=True)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    source = models.ForeignKey(Source, verbose_name="источник", on_delete=models.SET_NULL, null=True, blank=True)
    source_raw_id = models.CharField(verbose_name="id в источнике", max_length=255, null=True, blank=True)
    output_type = models.CharField(
        verbose_name='тип решения для автотестов', max_length=255,
        choices=OUTPUT_TYPES, default=STR
    )
    tests = JSONField(verbose_name='автотесты', default=list, blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)

    def __str__(self):
        return self.title