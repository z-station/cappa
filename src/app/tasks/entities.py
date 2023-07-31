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


class CandidateData(TypedDict):

    """ Candidate data for request in antiplag service """

    uuid: str
    code: str


class PlagData(TypedDict):

    """ Candidate data with max plag value """

    uuid: str
    percent: int
