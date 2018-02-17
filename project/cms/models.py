# -*- coding: utf-8 -*-
from django.db import models
from catalog.models import CatalogBase
# TODO  СДЕЛАТЬ в админке название моделей русскими  //гугли джанго админ
from django.db import models
from tinymce.models import HTMLField


class Course(CatalogBase):
    """модель курса в БД"""
    class Meta:
            verbose_name = "Курс"
            verbose_name_plural = "Курсы"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)


class Topic(CatalogBase):
    """модель темы в БД"""
    class Meta:
            verbose_name = "Тема"
            verbose_name_plural = "Темы"
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    content = HTMLField(verbose_name="Теория курса", default="")


class Task(CatalogBase):
    """модель задач в БД"""
    class Meta:
            verbose_name = "Задание"
            verbose_name_plural = "Задачи"
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    leaf = True
