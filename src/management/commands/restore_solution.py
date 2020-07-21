from django.core.management import BaseCommand
from src.training.models import Solution
from datetime import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        bug_date = datetime.strptime('2020-07-12', '%Y-%m-%d')
        solutions = Solution.objects.filter(datetime__gt=bug_date, content='').exclude(last_changes='')
        for s in solutions:
            s.content = s.last_changes
            s.save()
