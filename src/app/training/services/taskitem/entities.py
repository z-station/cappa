from typing import (
    TypedDict,
    NamedTuple,
    Optional,
)


class Test(TypedDict):

    data_in: str
    data_out: str


class TestingData(NamedTuple):

    count_tests: Optional[int]
    count_passed_tests: Optional[int]
    testing_score: Optional[float]
