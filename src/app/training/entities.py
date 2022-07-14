from typing import TypedDict, Optional
from app.tasks.enums import ScoreMethod, SolutionType
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
    solution_type: SolutionType


class PlagCheckResult(TypedDict):

    percent: float
    reference: Optional[PlagCheckUser]
    candidate: Optional[PlagCheckUser]
