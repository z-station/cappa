from typing import TypedDict, Optional, List


class DebugResult(TypedDict):

    result: Optional[str]
    error: Optional[str]


class Test(TypedDict):

    id: int
    data_in: str
    data_out: str
    enabled: bool
    visible: bool


class TestResult(TypedDict):

    id: int
    ok: bool
    result: Optional[str]
    error: Optional[str]


class TestingResult(TypedDict):

    ok: bool
    tests: List[TestResult]
