from typing import Optional
from app.common.raw_sql.queries import SqlQueryObject
from app.tasks.enums import SolutionType


class CourseUserStatisticsMixin:

    def get_course_statistics_cte_where(self):
        return """
        WHERE s.user_id = %(user_id)s
          AND topic.course_id = %(course_id)s
          AND s.type = %(solution_type)s
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
                  JOIN training_taskitem t ON s.task_id = t.task_id
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
            'user_id': user_id,
            'version_hash': version_hash,
            'solution_type': SolutionType.COURSE,
        }

    @property
    def sql_template(self) -> str:
        return f"""
        {self.get_course_statistics_cte()}
            
        INSERT INTO training_courseuserstatistics (
          user_id,
          course_id,
          version_hash,
          data
        )
          SELECT
            %(user_id)s,
            %(course_id)s,
            %(version_hash)s,
            statistics_json 
          FROM course_statistics
        
        ON CONFLICT (user_id, course_id) 
          DO UPDATE SET (data, version_hash) = (
              (
                SELECT statistics_json 
                FROM course_statistics
              ),
              %(version_hash)s
          )

        RETURNING
          id,
          course_id,
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
            'user_id': user_id,
            'version_hash': version_hash,
            'solution_type': SolutionType.COURSE,
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

        INSERT INTO training_courseuserstatistics (
          user_id,
          course_id,
          version_hash,
          data
        )
          SELECT
            %(user_id)s,
            %(course_id)s,
            %(version_hash)s,
            statistics_json 
          FROM course_statistics

        ON CONFLICT (user_id, course_id) 
          DO UPDATE 
            SET data = (
            SELECT statistics_json
            FROM course_statistics
          )
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
            'user_id': user_id,
            'solution_type': SolutionType.COURSE,
        }

    @property
    def sql_template(self) -> str:
        return f"""
        {self.get_course_statistics_cte()}

        UPDATE training_courseuserstatistics SET data = statistics_json
        FROM course_statistics
        WHERE
          course_id = %(course_id)s
          AND user_id = %(user_id)s
        """
