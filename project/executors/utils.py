# -*- coding: utf-8 -*-
import json
from datetime import datetime
from project.executors.models import UserSolution


def create_or_update_solution(user, code, tests_result, content ):

    """ Создать/дополнить запись о решении задачи пользователем UserSolution
        """
    if user.is_anonymous:
        return False
    else:
        try:
            user_solution = UserSolution.objects.get(user=user, code=code)
        except UserSolution.DoesNotExist:
            user_solution = UserSolution(code=code, user=user)
            user_solution.save()
        details = user_solution.details
        new_solution = {
            "datetime": str(datetime.now()),                   # текущее время
            "content": content,                                # пользовательский код
            "tests_num": tests_result["num"],                  # количество тестов
            "tests_success_num": tests_result["success_num"],  # количество пройденных тестов
        }
        if tests_result["num"] == tests_result["success_num"]:
            new_solution_progress = 100  # прогресс 100%
        else:
            new_solution_progress = tests_result["success_num"] / (tests_result["num"]/100)  # прогресс в процентах

        # Если новое решение более успешное
        if new_solution_progress > user_solution.progress:
            user_solution.progress = new_solution_progress
            user_solution.details["best_solution_num"] = len(details["solutions"])  # обновить порядковый номер успешного решения
            user_solution.details["best_solution_tests"] = tests_result["data"] # обновить детали тестов успешного решения
        user_solution.details["solutions"].append(new_solution)
        user_solution.save()
        return True if user_solution.progress == 100 else False

