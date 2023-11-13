# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TrainingAppConfig(AppConfig):

    name = "app.training"
    verbose_name = 'Разделы сайта'

    def ready(self):
        import app.training.signals
