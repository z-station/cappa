# -*- coding: utf-8 -*-
from django.test import TestCase
from src.langs.models import Lang
from src.tasks.models import Task
from src.training.models.taskitem import Solution
from src.utils.db import load_dump, remove_db_objects


class ProviderTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('===> reset db')
        remove_db_objects()
        load_dump()

    def test_provider(self):

        """ Прогон python по тестовой выборке задач """

        print('===> RUN Python tests')
        provider = Lang.objects.get(provider_name=Lang.PYTHON).provider
        for task in Task.objects.all():
            solution = Solution.objects.filter(
                taskitem__task=task,
                taskitem__topic__course__lang__provider_name=Lang.PYTHON
            ).first()
            if solution and solution.status == Solution.S__SUCCESS:
                tests_result = provider.check_tests(
                    content=solution.version_best['content'],
                    task=task
                )
                self.assertTrue(
                    expr=tests_result['success'],
                    msg=f'id={task.id}, title="{task.title}"'
                )
