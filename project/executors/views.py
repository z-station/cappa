# -*- coding:utf-8 -*-
import json
from datetime import datetime
from django.shortcuts import HttpResponse, render
from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, CodeSolution,  PYTHON36, MAXIMIZED, EXECUTE, CHECK_TESTS

# TODO обработчик для сохранения попыток


def update_user_solution(type, user, code, content, input="", tests_result=None):

    """ Создать/дополнить запись о решении задачи пользователем CodeSolution
        Пока есть 2 типа решений:
           1. тип: EXECUTE = 1 простой запуск
           2. тип: CHECK_TESTS = 2 запуск тестов
           фиксируется количество запусков обоих типов для статистики
    """
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

    if type == EXECUTE:
        new_solution["success"] = False
        code_solution.execute_count += 1

    elif type == CHECK_TESTS:
        total_success = True
        for test in tests_result:
            new_solution["tests"].append({
                "id": test["id"],
                "success": test["success"],
            })
            total_success = total_success and test["success"]
        new_solution["success"] = total_success
        code_solution.check_tests_count += 1
        code_solution.success = total_success

    details = json.loads(code_solution.details)
    details["solutions"].append(new_solution)
    code_solution.details = json.dumps(details, ensure_ascii=False)
    code_solution.save()
    return code_solution.success


def execute(request):
    """ Контроллер обработки асинхронных запусков кода
        - Исполняет код в исполнителе (указанного для кода)
        - Обновляет запись пользовательского решения (если указанно для кода)
        - возвращает результаты пользователю
    """
    try:
        code_id = request.POST.get("code_id")
        code = Code.objects.get(id=code_id)
    except Code.DoesNotExist:
        return HttpResponse("OOPS! SOMETHING WENT WRONG!!")
    else:
        content = request.POST.get("content")
        input, output, error = request.POST.get("input", ""), "", ""
        code_solved = False
        tests = CodeTest.objects.filter(code=code)
        if content:
            if code.get_executor_type_id() == PYTHON36:
                from project.executors.python36.utils import execute_code
                output, error = execute_code(code, content, input)
                code_solved = update_user_solution(EXECUTE, request.user, code, content, input)

        form = CodeForm(initial={
            "content": content,
            "input": input,
            "output": output,
            "error": error,
        })
        context = {
            "code_solved": code_solved,
            "tests": tests,
            "form": form,
            "code_id": code_id,
            "code_num": request.POST.get("code_num"),
        }
        return render(request, code.get_template(), context)


def check_tests(request):
    """ Контроллер обработки асинхронных запусков тестирования кода
        - Исполняет код в исполнителе (указанного для кода)
        - Обновляет запись пользовательского решения, добавляет инф. по тестам (если указанно для кода)
        - возвращает результаты пользователю (включая результаты по тестам)
    """
    try:
        code_id = request.POST.get("code_id")
        code = Code.objects.get(id=code_id)
    except Code.DoesNotExist:
        return HttpResponse("OOPS! SOMETHING WENT WRONG!!")
    else:
        content = request.POST.get("content")
        input, output, error = request.POST.get("input", ""), "", ""
        tests = CodeTest.objects.filter(code=code)
        tests_result = []
        if content and tests and code.type == MAXIMIZED:
            if code.get_executor_type_id() == PYTHON36:
                from project.executors.python36.utils import check_tests
                tests_result = check_tests(code, content, tests)
                update_user_solution(CHECK_TESTS, request.user, code, content, "", tests_result)

        form = CodeForm(initial={
            "content": content,
            "input": input,
            "output": output,
            "error": error,
        })
        context = {
            "tests_result": tests_result,
            "tests": tests,
            "form": form,
            "code_id": code_id,
            "code_num": request.POST.get("code_num"),
        }
        return render(request, code.get_template(), context)
