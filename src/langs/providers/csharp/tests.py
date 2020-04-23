# -*- coding: utf-8 -*-
from django.test import TestCase
from src.utils.db import load_dump, remove_db_objects


class ProviderTestCase(TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     print('===> reset db')
    #     remove_db_objects()
    #     load_dump()

    def test_providers(self):

        # TODO написать тесты для C#

        print('===> RUN C# tests')
