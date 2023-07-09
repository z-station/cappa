from typing import Optional
from app.common.raw_sql.queries import SqlQueryObject
from app.tasks.enums import TaskItemType


class CourseUserStatisticsMixin:

    def get_course_statistics_cte_where(self):
        return """
        WHERE s.user_id = %(user_id)s
          AND topic.course_id = %(course_id)s
          AND s.type = %(course_type)s
          AND s.type_id = %(course_id)s """

    def get_course_statistics_cte(self):
        """ Возвращает таблицу, где каждая запись это пара:
            id задачи курса (taskitem_id) и статистика решений пользователя
            по этой задаче курса """

        return f"""
        WITH course_statistics AS (
            SELECT COALESCE(
                json_object_agg(taskitem_id, value),
                '{{}}'::json
              ) AS statistics_json
            FROM (
                SELECT DISTINCT ON (s.user_id, s.task_id)
                  t.id AS taskitem_id,
                  json_build_object(
                    'created', s.created,
                    'translator', s.translator,
                    'due_date', s.due_date,
                    'id', s.id,
                    'testing_score', s.testing_score,
                    'review_status', s.review_status,
                    'review_score', (
                      CASE 
                        WHEN s.hide_review_score IS FALSE THEN s.review_score
                        ELSE NULL
                      END
                    ),
                    'score_method', t.score_method,
                    'max_score', t.max_score
                  ) AS value
                FROM tasks_solution s
                  JOIN tasks_taskitem t ON s.task_id = t.task_id
                  JOIN training_topic topic ON t.topic_id = topic.id
    
                {self.get_course_statistics_cte_where()}
    
                ORDER BY s.user_id, s.task_id, s.created DESC
            ) taskitem_raw_statistics
        )
        """


class CreateOrUpdateCourseUserStatisticsQuery(
    CourseUserStatisticsMixin,
    SqlQueryObject
):

    def __init__(
            self,
            course_id: int,
            user_id: int,
            version_hash: str,
    ):
        self.sql_params = {
            'course_id': course_id,
            'course_type': TaskItemType.COURSE,
            'user_id': user_id,
            'version_hash': version_hash,
        }

    @property
    def sql_template(self) -> str:
        return f"""
        {self.get_course_statistics_cte()}
            
        INSERT INTO tasks_userstatistics (
          user_id,
          type_id,
          type,
          version_hash,
          data
        )
          SELECT
            %(user_id)s,
            %(course_id)s,
            %(course_type)s,
            %(version_hash)s,
            statistics_json 
          FROM course_statistics
        
        ON CONFLICT (user_id, type_id, type) 
          DO UPDATE SET (data, version_hash) = (
              (
                SELECT statistics_json 
                FROM course_statistics
              ),
              %(version_hash)s
          )

        RETURNING
          id,
          type_id,
          user_id,
          version_hash,
          data
        """


class CreateOrUpdateUserTaskItemStatisticQuery(
    CreateOrUpdateCourseUserStatisticsQuery
):

    def __init__(
            self,
            course_id: int,
            user_id: int,
            version_hash: str,
            taskitem_id: Optional[int] = None
    ):
        self.sql_params = {
            'course_id': course_id,
            'course_type': TaskItemType.COURSE,
            'user_id': user_id,
            'version_hash': version_hash,
            'taskitem_id': taskitem_id,
        }

    def get_course_statistics_cte_where(self) -> str:
        return (
                super().get_course_statistics_cte_where() +
                "AND t.id = %(taskitem_id)s"
        )

    @property
    def sql_template(self) -> str:
        return f"""
        {self.get_course_statistics_cte()}

        INSERT INTO tasks_userstatistics (
          user_id,
          type_id,
          type,
          version_hash,
          data
        )
          SELECT
            %(user_id)s,
            %(course_id)s,
            %(course_type)s,
            %(version_hash)s,
            statistics_json 
          FROM course_statistics

        ON CONFLICT (user_id, type_id, type) 
          DO UPDATE 
            SET data = tasks_userstatistics.data || (
            SELECT statistics_json
            FROM course_statistics
          )::jsonb
        """


class UpdateCourseUserStatisticsQuery(
    CourseUserStatisticsMixin,
    SqlQueryObject
):

    def __init__(
            self,
            course_id: int,
            user_id: int,
    ):
        self.sql_params = {
            'course_id': course_id,
            'course_type': TaskItemType.COURSE,
            'user_id': user_id,
        }

    @property
    def sql_template(self) -> str:
        return f"""
        {self.get_course_statistics_cte()}

        UPDATE tasks_userstatistics SET data = statistics_json
        FROM course_statistics
        WHERE
          type_id = %(course_id)s
          AND type = %(course_type)s
          AND user_id = %(user_id)s
        """


class UpdateRatingQuery(
    SqlQueryObject
):
    sql_template = """
        WITH new_rating AS (
            SELECT
                id,
                (1 - rating_success / rating_total) * 100 AS rating,
                rating_success,
                rating_total
            FROM (
                SELECT 
                    t.id AS id,
                    CAST(
                        t.rating_success + (COUNT(s.id) FILTER(WHERE s.score = s.max_score)) AS real
                    ) AS rating_success,
                    CAST(t.rating_total + COUNT(s.id) AS real) AS rating_total
                FROM
                    tasks_solution s INNER JOIN tasks_task t
                        ON s.task_id = t.id
                WHERE
                    s.rating_is_calculated = FALSE
                GROUP BY
                    t.id
            ) rating_tasks
        )
        UPDATE tasks_task
        SET rating = nr.rating,
            rating_success = nr.rating_success,
            rating_total = nr.rating_total
        FROM new_rating nr
        WHERE tasks_task.id = nr.id
    """
