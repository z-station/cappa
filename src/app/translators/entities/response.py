from typing import TypedDict, List, Union


class ResponseTestData(TypedDict):

    test_console_input: str
    test_console_output: str
    translator_console_output: str
    translator_error_msg: str
    ok: Union[bool, None]


class ResponseTestingDict(TypedDict):

    num: int
    num_ok: int
    ok: bool
    tests_data: List[ResponseTestData]
