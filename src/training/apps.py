# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TrainingAppConfig(AppConfig):

    name = "src.training"
    verbose_name = 'Учебные курсы'

    def ready(self):
        import src.training.signals
