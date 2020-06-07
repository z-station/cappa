from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from src.quizzes.models import Solution, TaskItem


@receiver(post_save, sender=Solution)
@receiver(post_delete, sender=Solution)
def solution_saved_handler(sender, instance, **kwargs):
    instance.user.update_cache_quiz_solutions_data(
        quiz=instance.taskitem.quiz,
    )


@receiver(post_save, sender=TaskItem)
@receiver(post_delete, sender=TaskItem)
def taskitem_changed_handler(sender, instance, **kwargs):
    post_save.disconnect(taskitem_changed_handler, sender=TaskItem)
    number = 1
    for taskitem in TaskItem.objects.filter(show=True, quiz=instance.quiz):
        taskitem.number = number
        taskitem.save()
        number += 1
    post_save.connect(taskitem_changed_handler, sender=TaskItem)
    cache.clear()

