from datetime import datetime
from typing import TypedDict, Optional
from app.tasks.enums import ScoreMethod, TaskItemType
from app.translators.enums import TranslatorType


class TaskItemStatistics(TypedDict):

    id: int
    created: str
    translator: TranslatorType
    score_method: ScoreMethod
    max_score: int
    review_status: Optional[str]
    review_score: Optional[str]
    testing_score: Optional[str]
    due_in: Optional[str]


class PlagCheckUser(TypedDict):

    id: int
    solution_id: int
    solution_type: TaskItemType


class PlagCheckResult(TypedDict):

    percent: float
    datetime: datetime
    reference: Optional[PlagCheckUser]
    candidate: Optional[PlagCheckUser]
