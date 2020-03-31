from django.core.management import BaseCommand
from src.training.models import Solution


class Command(BaseCommand):

    def update_version(self, old_version, max_score) -> dict:
        if old_version.get('tests_score') is None:
            if old_version['progress'] is not None:
                tests_score = round(int(old_version['progress']) / 100 * max_score, 2)
            else:
                tests_score = None
            return {
                "datetime": old_version['datetime'],
                "content": old_version['content'],
                "tests_score":  tests_score
            }
        else:
            return old_version

    def handle(self, *args, **options):
        for s in Solution.objects.all():
            try:
                if s.version_best:
                    s.version_best = self.update_version(
                        old_version=s.version_best,
                        max_score=s.taskitem.max_score
                    )
                else:
                    self.stdout.write(self.style.WARNING(f'{s}: version_best: {s.version_best} : {type(s.version_best)}'))
                updated_version_list = []
                if s.version_list:
                    for v in s.version_list:
                        updated_version_list.append(self.update_version(
                            old_version=v,
                            max_score=s.taskitem.max_score)
                        )
                    s.version_list = updated_version_list
                if hasattr(s, 'progress') and s.progress is not None:
                    s.tests_score = round(int(s.progress) / 100 * s.taskitem.max_score, 2)
                s.save()
                self.stdout.write(self.style.SUCCESS(f'{s}: {s.score}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{s}: {e}'))
                raise