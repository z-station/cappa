import requests
from app.translators.consts import translators_internal_urls
from app.translators.checkers import checkers
from app.translators.entities.request import (
    RequestTestData,
    RequestTestingDict
)
from app.translators.entities.response import (
    SandboxResponseData,
    SandboxErrorData
)
from app.training.models import TaskItem


def testing(code: str, taskitem: TaskItem) -> SandboxResponseData:

    """ Прогон кода на тестах задачи
        Передает данные для тестирования в сервис-песочницу
        и возвращает результаты тестирования
    """
    translator = taskitem.translator
    checker = taskitem.task.output_type
    tests_data = [
        RequestTestData(
            test_console_input=test['input'],
            test_console_output=test['output']
        ) for test in taskitem.task.tests
    ]
    data = RequestTestingDict(
        checker_code=checkers[checker],
        tests_data=tests_data,
        code=code
    )
    host = translators_internal_urls[translator]
    url = f'{host}/testing/'
    try:
        response = requests.post(
            url=url,
            json=data
        )
    except Exception as e:
        result = SandboxResponseData(
            ok=False,
            error=SandboxErrorData(
                msg='Транслятор кода недоступен (500)',
                details=str(e)
            )
        )
    else:
        if response.ok:
            result = SandboxResponseData(
                ok=True,
                data=response.json()
            )
        else:
            result = SandboxResponseData(
                ok=False,
                error=SandboxErrorData(
                    msg=f'Транслятор кода недоступен ({response.status_code})'
                )
            )
    return result
