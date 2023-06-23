from django.db.models import Count

from app.tasks.models import Solution


def calculate_rating():
    # TODO queryset не проверен
    # SELECT task, score, max_score, COUNT(task) AS task_count
    # WHERE rating_is_calculated = False
    # FROM solution GROUP BY task
    qs = (
        Solution.objects
        .values('task', 'score', 'max_score')
        .annotate(task_count=Count('task'))
        .filter(rating_is_calculated=False)
        .order_by()
    )
    for solution in qs:
        task = solution['task']
        score = solution['score']
        max_score = solution['max_score']
        task_count = solution['task_count']

        # TODO если групперуем по задачам,
        #  то как установить флаг для этих решений, что они учтены в рейтинге?
        solution.rating_is_calculated = True
        solution.save()

        task.rating_total += task_count
        if score == max_score:
            task.rating_success += task_count

        task.rating = (1 - task.rating_success / task.rating_total) * 100
    # qs берем все не учтенные в рейтинге решения, группируя их по задачам, считая успешные и неуспешные
    # возможно лучше использовать не qs, а SQL запрос
    #
    # Для всех решений проставляем поле что они учтены для рейтинга
    # Для всех задач, которые получили в результате группировки обновляем рейтинг

