from typing import TypedDict, Optional
from app.tasks.enums import ScoreMethod
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
