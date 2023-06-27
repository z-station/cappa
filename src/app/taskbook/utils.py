from django.db import transaction


@transaction.atomic()
def calculate_rating():
    f"""
        WITH solutions_list AS (
            SELECT task_id AS id, score, max_score
            FROM solution
            WHERE rating_is_calculated = False
        ),
        
        count_success AS (
            SELECT id, CAST(COUNT(*) AS real) AS success
            FROM solutions_list
            WHERE score = max_score
            GROUP BY id
        ),
        
        count_total AS (
            SELECT id, CAST(COUNT(*) AS real) AS total
            FROM solutions_list
            GROUP BY id
        ),
        
        group_by_task AS (
            SELECT count_total.id, COALESCE(success, 0) AS success, total
            FROM count_total LEFT JOIN count_success
            ON count_total.id = count_success.id
        ),
        
        get_task_info AS (
            SELECT id, rating_success, rating_total
            FROM tasks
            WHERE id in (SELECT id FROM group_by_task)
        ),
        
        get_new_rating AS (
            SELECT get_task_info.id,
            (1 - (rating_success + success) / (rating_total + total)) * 100 AS rating,
            success, total
            FROM get_task_info JOIN group_by_task
            ON get_task_info.id = group_by_task.id
        ),
        
        update_rating AS (
            UPDATE tasks
            SET rating = get_new_rating.rating,
                rating_success = rating_success + success,
                rating_total = rating_total + total
            FROM get_new_rating
            WHERE tasks.id = get_new_rating.id
        ),
        
        update_solutions AS (
            UPDATE solutions
            SET rating_is_calculated = True
            WHERE rating_is_calculated = False
        )
    """
