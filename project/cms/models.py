# -*- coding: utf-8 -*-
from django.db import models
from catalog.models import CatalogBase
from django.db import models
from tinymce.models import HTMLField
from project.executors.models import Executor


class Course(CatalogBase):
    """модель курса в БД"""
    class Meta:
            verbose_name = "Курс"
            verbose_name_plural = "Курсы"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    # short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    executors = models.ManyToManyField(Executor)

    def __str__(self):
        return self.title


class Topic(CatalogBase):
    """модель темы в БД"""
    class Meta:
            verbose_name = "Тема"
            verbose_name_plural = "Темы"
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    # short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    content = HTMLField(verbose_name="Теория курса", default="")

    def __str__(self):
        return self.title


class Task(CatalogBase):
    """модель задач в БД"""
    class Meta:
            verbose_name = "Задание"
            verbose_name_plural = "Задачи"
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(verbose_name="url", unique=True, max_length=255)
    long_title = models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True, null=True)
    # short_desc = models.TextField(verbose_name="Краткое описание", blank=True, null=True)
    content = HTMLField(verbose_name="Текст задания", default="")
    leaf = True

    def __str__(self):
        return self.title
