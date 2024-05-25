# -*- coding: utf-8 -*-
from django.db import models
from app.common.fields import OrderField
from app.common.fields import AnyExtFileBrowseField


class Menu(models.Model):

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = verbose_name

    TOP = 'top'
    SIDEBAR = 'sidebar'
    CHOICES = (
        (TOP, 'в шапке'),
        (SIDEBAR, 'в сайдбаре'),
    )

    name = models.CharField(verbose_name='Название', max_length=255)
    key = models.CharField(
        verbose_name='тип меню', max_length=255,
        choices=CHOICES, unique=True,
    )

    def __str__(self):
        return self.name


class MenuItem(models.Model):

    class Meta:
        verbose_name = 'пункт меню'
        verbose_name_plural = 'пункты меню'
        ordering = ('order_key',)

    order_key = OrderField(verbose_name='порядок', blank=True,  null=True, for_fields=['course'])
    menu = models.ForeignKey(Menu, related_name='menuitems')
    name = models.CharField(verbose_name='текст', max_length=255)
    url = models.CharField(verbose_name='ссылка', max_length=255)
    image = AnyExtFileBrowseField(
        verbose_name='изображение',
        max_length=1000,
        blank=True,
        null=True
    )

    show = models.BooleanField(verbose_name='отображать', default=True)

    def __str__(self):
        return self.name


__all__ = ('Menu', 'MenuItem')
