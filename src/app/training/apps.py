# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TrainingAppConfig(AppConfig):

    name = "app.training"
    verbose_name = 'Учебные курсы'

    def ready(self):
        import app.training.signals
