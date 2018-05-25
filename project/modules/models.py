from django.contrib.auth.models import User
from django.db import models

from project.courses.models import TreeItem


class Module(models.Model):
    name = models.CharField(max_length=64, help_text='Введите название модуля', verbose_name='Название')
    comment = models.TextField(help_text='Введите комментарий к модулю', verbose_name='Комментарий', blank=True)
    owner = models.ForeignKey(User, verbose_name='Владелец', related_name='modules')
    tasks = models.ManyToManyField(TreeItem, blank=True)
    updated_at = models.DateTimeField(verbose_name='Изменен', auto_now=True)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.name

    def get_tasks_number(self):
        return self.tasks.count()

    get_tasks_number.short_description = 'Задач'
