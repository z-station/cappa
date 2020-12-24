from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.training.models import Course


@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Course)
def course_changed_handler(sender, instance, **kwargs):
    cache.clear()
