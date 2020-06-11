# -*- coding: utf-8 -*-
from django.test import TestCase
from src.langs.models import Lang
from src.tasks.models import Task
from src.training.models.taskitem import Solution
from src.utils.db import load_dump, remove_db_objects


class ProviderTestCase(TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     print('===> reset db')
    #     remove_db_objects()
    #     load_dump()

    def test_provider(self):
        print('===> RUN SQL tests')
