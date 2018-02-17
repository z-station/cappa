# -*- coding:utf-8 -*-
from django.db import models


class Executor(models.Model):
    class Meta:
        verbose_name = "Исполнитель кода"
        verbose_name_plural = "Исполнители кода"

    AVAILABLE_EXECUTORS = (
        (0, "Python 3.6"),
        (1, "Test 1"),
        (2, "Test 2"),
    )
    name = models.IntegerField(
        verbose_name="Наименование",
        max_length=255,
        unique=True,
        choices=AVAILABLE_EXECUTORS,
    )

    def __str__(self):
        return self.AVAILABLE_EXECUTORS[self.name][1]
