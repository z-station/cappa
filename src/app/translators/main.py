import json
import requests
from app.tasks.models import Task
from app.translators.consts import ts_hosts
from app.translators.checkers import checkers
from app.translators.entities.request import (
    RequestTestData,
    RequestTestingDict
)


def testing(code: str, task: Task, translator: int):
    data = RequestTestingDict(
        checker_code=checkers[task.output_type],
        tests_data=[
            RequestTestData(
                test_console_input=test['input'],
                test_console_output=test['output']
            ) for test in task.tests
        ],
        code=code
    )
    host = ts_hosts[translator]
    url = f'{host}/testing/'
    response = requests.post(
        url=url,
        json=json.dumps(data, ensure_ascii=False)
    )
    if response.ok:
        return response.json()
