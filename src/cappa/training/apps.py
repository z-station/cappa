# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TrainingAppConfig(AppConfig):

    name = "cappa.training"
    verbose_name = 'Учебные курсы'

    def ready(self):
        import cappa.training.signals
