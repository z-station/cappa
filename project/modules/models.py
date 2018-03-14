from django.db import models
from django.contrib.auth.models import User

from project.cms.fields import JSONField
from project.cms.models import Course


class Module(models.Model):
    name = models.CharField(max_length=64, help_text="Введите название модуля", verbose_name="Название")
    owner = models.ForeignKey(User, verbose_name="Владелец")
    courses = models.ManyToManyField(Course, blank=True)
    units = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return self.name
