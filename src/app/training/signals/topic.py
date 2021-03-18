from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.training.models import Topic


@receiver(post_delete, sender=Topic)
@receiver(post_save, sender=Topic)
def topic_changed_handler(sender, instance, **kwargs):
    post_save.disconnect(topic_changed_handler, sender=Topic)
    number = 1
    for topic in Topic.objects.filter(show=True, course=instance.course):
        topic.number = number
        topic.save()
        number += 1
    post_save.connect(topic_changed_handler, sender=Topic)
    cache.clear()
