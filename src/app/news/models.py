# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class News(models.Model):

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-date']

    title = models.CharField(verbose_name='заголовок', max_length=255)
    date = models.DateField(verbose_name='дата создания')
    content = HTMLField(verbose_name="описание", blank=True, null=True)
    author = models.ForeignKey(User, verbose_name='автор', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение')
    show = models.BooleanField(verbose_name='показывать', default=False)

    def __str__(self):
        """ Строкове представление """
        return self.title
