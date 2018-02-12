# -*- coding: utf-8 -*-
from django.db import models
from catalog.models import CatalogBase
# TODO  СДЕЛАТЬ в админке название моделей русскими  //гугли джанго админ

class Course(CatalogBase):
    """модель курса в БД"""
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)


class Topic(CatalogBase):
    """модель темы в БД"""
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)


class Task(CatalogBase):
    """модель задач в БД"""
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    leaf = True
