import json
import requests
from app.translators.consts import translators_hosts
from app.translators.checkers import checkers
from app.translators.entities.request import (
    RequestTestData,
    RequestTestingDict
)
from app.translators.entities.response import ResponseTestingDict
from app.training.models import TaskItem


def testing(code: str, taskitem: TaskItem) -> ResponseTestingDict:

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
    host = translators_hosts[translator]
    url = f'{host}/testing/'
    response = requests.post(
        url=url,
        json=data
    )
    if response.ok:
        return response.json()
