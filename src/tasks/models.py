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

    order_key = models.PositiveIntegerField(verbose_name='порядок', default=0)
    show = models.BooleanField(verbose_name="отображать", default=False)
    last_modified = models.DateTimeField(verbose_name="дата последнего изменения", auto_now=True)
    title = models.CharField(verbose_name="заголовок", max_length=255)
    author = models.ForeignKey(UserModel, verbose_name="автор", on_delete=models.SET_NULL, blank=True, null=True)
    content = HTMLField(verbose_name="текст задания", default="", blank=True, null=True)
    source = models.ForeignKey(Source, verbose_name="источник", on_delete=models.SET_NULL, null=True, blank=True)
    source_raw_id = models.CharField(verbose_name="id в источнике", max_length=255, null=True, blank=True)
    tests = JSONField(verbose_name='тесты', default=list, blank=True, null=True)

    def __str__(self):
        return self.title