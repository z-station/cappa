# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from project.executors.models import UserSolution


class Command(BaseCommand):

    """ Обновить структуру решений (единовременная процедура)"""

    def handle(self, *args, **options):
        for s in UserSolution.objects.all():
            d = s.details
            num = d.get('best_solution_num')
            if not num:
                num = len(d['solutions'])-1
            data = d['solutions'][num]
            version = {
                "datetime": data['datetime'],
                "input": data.get('input', ''),
                "content": data['content'],
                "progress":  round(data["tests_success_num"] / (data["tests_num"] / 100)),
                "tests": {
                    'num': data.get("tests_num", ''),
                    'num_success': data.get("tests_success_num", ''),
                }
            }
            s.update_best(version=version)
            s.save()
