# -*- coding: utf-8 -*-
from django.test import TestCase
from src.langs.models import Lang
from src.tasks.models import Task
from src.training.models.taskitem import Solution
from src.utils.db import load_dump, remove_db_objects
from src.utils.consts import langs


class ProviderTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('===> reset db')
        remove_db_objects()
        load_dump()

    def test_provider(self):

        """ Прогон python по тестовой выборке задач """

        print('===> RUN Python tests')
        provider = Lang.objects.get(provider_name=langs.PYTHON).provider

        # Задачи, тесты которых должны закончиться успехом
        for task in Task.objects.filter(lang=langs.PYTHON, tags__name='success'):
            solution = task.solution_examples.filter(lang=langs.PYTHON).first()
            tests_result = provider.check_tests(content=solution.content, task=task)
            self.assertTrue(
                expr=tests_result['success'],
                msg=f'id={task.id}, title="{task.title}"'
            )
            print(f'===> SUCCESS: {task}')

        # Задачи, тесты которых должны провалиться
        for task in Task.objects.filter(lang=langs.PYTHON, tags__name='unluck'):
            solution = task.solution_examples.filter(lang=langs.PYTHON).first()
            tests_result = provider.check_tests(content=solution.content, task=task)
            self.assertFalse(
                expr=tests_result['success'],
                msg=f'id={task.id}, title="{task.title}"'
            )
            print(f'===> UNLUCK: {task}')
