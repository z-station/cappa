# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from project.courses.models import TreeItem


class Module(models.Model):

    class Meta:
        verbose_name = 'oлимпиада'
        verbose_name_plural = 'oлимпиады'

    name = models.CharField(max_length=64, help_text='Введите название', verbose_name='Название')
    comment = models.TextField(max_length=1024, help_text='Введите комментарий', verbose_name='Комментарий', blank=True, null=True)
    owner = models.ForeignKey(User, verbose_name='Владелец', related_name='modules', null=True, on_delete=models.SET_NULL)
    treeitems = models.ManyToManyField(TreeItem, verbose_name="задачи", blank=True, limit_choices_to={"leaf": True})
    updated_at = models.DateTimeField(verbose_name='Изменен', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('modules:module', args=(self.pk, ))
