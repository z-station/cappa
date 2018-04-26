from django.contrib.auth.models import User
from django.db import models

from project.cms.models import Task


class Module(models.Model):
    name = models.CharField(max_length=64, help_text="Введите название модуля", verbose_name="Название")
    owner = models.ForeignKey(User, verbose_name="Владелец")
    tasks = models.ManyToManyField(Task, blank=True)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.name
