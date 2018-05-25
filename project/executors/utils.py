# -*- coding: utf-8 -*-
import json
from datetime import datetime
from project.executors.models import CodeSolution


def create_or_update_solution(type, user, code, content, input="", tests_result=None):

    """ Создать/дополнить запись о решении задачи пользователем CodeSolution
        Пока есть 2 типа решений:
           1. тип: EXECUTE = 1 простой запуск
           2. тип: CHECK_TESTS = 2 запуск тестов
           фиксируется количество запусков обоих типов для статистики
    """
    if user.is_anonymous:
        return False
    else:
        try:
            code_solution = CodeSolution.objects.get(user=user, code=code)
        except CodeSolution.DoesNotExist:
            code_solution = CodeSolution(code=code, user=user)
            code_solution.save()

        new_solution = {
            "type": type,
            "datetime": str(datetime.now()),
            "input": input,
            "content": content,
            "tests": [],
        }

        if type == CodeSolution.EXECUTE:
            new_solution["success"] = False
            code_solution.execute_count += 1

        elif type == CodeSolution.CHECK_TESTS:
            total_success = True
            for test in tests_result:
                new_solution["tests"].append({
                    "id": test["id"],
                    "success": test["success"],
                })
                total_success = total_success or test["success"]  # если уже было удачное решение то не перезаписывать
            new_solution["success"] = total_success
            code_solution.check_tests_count += 1
            code_solution.success = total_success

        details = json.loads(code_solution.details)
        details["solutions"].append(new_solution)
        code_solution.details = json.dumps(details, ensure_ascii=False)
        code_solution.save()
        return code_solution.success

