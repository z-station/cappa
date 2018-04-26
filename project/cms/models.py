# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, NoReverseMatch
from catalog.models import CatalogBase
from django.db import models
from tinymce.models import HTMLField


# TODO Ирке создать базовый класс
class CmsBase(CatalogBase):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    content = HTMLField(verbose_name="Содержимое", default="", blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        path = self.get_complete_slug()
        if path:
            try:
                return reverse('cms-item', kwargs={'path': path})
            except NoReverseMatch:
                pass
        else:
            return ''


class Course(CmsBase):
    """модель курса"""
    class Meta:
            verbose_name = "Курс"
            verbose_name_plural = "Курсы"


class Topic(CmsBase):
    """модель темы"""
    class Meta:
            verbose_name = "Тема"
            verbose_name_plural = "Темы"


class Task(CmsBase):
    """модель задач"""
    class Meta:
            verbose_name = "Задание"
            verbose_name_plural = "Задачи"

    leaf = True
