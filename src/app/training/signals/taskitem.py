from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.training.models import TaskItem


@receiver(post_save, sender=TaskItem)
@receiver(post_delete, sender=TaskItem)
def taskitem_changed_handler(sender, instance, **kwargs):
    post_save.disconnect(taskitem_changed_handler, sender=TaskItem)
    number = 1
    for taskitem in TaskItem.objects.filter(show=True, topic=instance.topic):
        taskitem.number = number
        taskitem.save(update_fields=('number',))
        number += 1
    post_save.connect(taskitem_changed_handler, sender=TaskItem)
    cache.clear()

