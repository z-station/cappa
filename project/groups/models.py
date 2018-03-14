from django.db import models
from django.contrib.auth.models import User

from project.cms.fields import JSONField
from project.modules.models import Module


class Group(models.Model):
    name = models.CharField(max_length=64, help_text="Введите название группы", verbose_name="Название")
    owners = models.ManyToManyField(User, verbose_name="Владельцы", related_name='ownership')
    members = models.ManyToManyField(User, verbose_name="Пользователи", related_name='membership', blank=True)
    modules = models.ManyToManyField(Module, verbose_name="Модули", blank=True)
    progress = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name

    def display_root_owner(self):
        return self.owners.all()[0].username

    display_root_owner.short_description = 'Владелец'
