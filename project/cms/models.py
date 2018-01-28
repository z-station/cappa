# -*- coding: utf-8 -*-
from mptt.models import MPTTModels
from django.db import models

class Cource(MPTTModels):
    title=models.CharField(max_length=255, verbose_name="Заголовок")
    long_title=models.CharField(max_length=255, verbose_name="Длинный заголовок", blank=True,null=True)
    short_desc=models.TextField(verbose_name="Краткое описание", blank=True,null=True)
