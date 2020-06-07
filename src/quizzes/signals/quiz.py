from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from src.quizzes.models import Quiz


@receiver(post_save, sender=Quiz)
@receiver(post_delete, sender=Quiz)
def quiz_changed_handler(sender, instance, **kwargs):
    cache.clear()
