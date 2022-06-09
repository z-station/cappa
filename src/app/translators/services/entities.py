from typing import TypedDict, Optional, List


class DebugResult(TypedDict):

    result: Optional[str]
    error: Optional[str]


class Test(TypedDict):

    data_in: str
    data_out: str


class TestResult(TypedDict):

    ok: bool
    result: Optional[str]
    error: Optional[str]


class TestingResult(TypedDict):

    ok: bool
    tests: List[TestResult]
