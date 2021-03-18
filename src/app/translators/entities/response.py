from typing import TypedDict, List, Union, Optional

ERROR = 'error'
WARNING = 'warning'
OK = 'ok'

RESPONSE_STATUSES = {
    ERROR,
    WARNING,
    OK
}


class SandboxResponseTestData(TypedDict):

    """ Содержит данные о результатах выполнения теста в песочнице """

    test_console_input: str
    test_console_output: str
    translator_console_output: str
    translator_error_msg: str
    ok: Union[bool, None]


class SandboxResponseTestingDict(TypedDict):

    """ Ответ песочницы, содержит данные о результатах тестирования """

    ok: bool
    num: int
    num_ok: int
    tests_data: List[SandboxResponseTestData]


class SandboxErrorData(TypedDict):

    msg: str
    details: Optional[str]


class SandboxResponseData(TypedDict):

    """ Содержит данные о результатах запроса к песочнице """

    ok: bool
    error: Optional[SandboxErrorData]
    data: Optional[SandboxResponseTestingDict]


class OperationResponse(TypedDict):

    """ Ответ приложения, содержит данные о результатах запроса к приложению """

    msg: str
    status: str
    sandbox_data: Optional[SandboxResponseData]

