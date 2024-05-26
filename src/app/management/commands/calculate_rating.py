from django.core.management import BaseCommand
from app.tasks.utils import calculate_rating


class Command(BaseCommand):

    def handle(self, *args, **options):
        calculate_rating()