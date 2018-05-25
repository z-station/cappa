# -*- coding:utf-8 -*-

from django.shortcuts import HttpResponse, render
from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, CodeSolution, Executor
from project.executors.utils import create_or_update_solution


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
        return HttpResponse("Code does not exist")
    else:
        content = request.POST.get("content")
        input, output, error = request.POST.get("input", ""), "", ""
        code_solved = False
        tests = CodeTest.objects.filter(code=code)
        if content:
            if code.get_executor_type_id() == Executor.PYTHON36:
                from project.executors.python36.utils import execute_code
                output, error = execute_code(code, content, input)
                if code.save_solutions and not request.user.is_anonymous:
                    code_solved = create_or_update_solution(CodeSolution.EXECUTE, request.user, code, content, input)

        form = CodeForm(initial={
            "content": content,
            "input": input,
            "output": output,
            "error": error,
        })
        context = {
            "code_solved": code_solved,
            "form": form,
            "code_num": request.POST.get("code_num"),
            "code_id": code_id,
            "show_tests": code.show_tests,
            "show_input": code.show_input,
            "tests": tests,
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
        return HttpResponse("Code does not exist")
    else:
        content = request.POST.get("content")
        input, output, error = request.POST.get("input", ""), "", ""
        code_solved = False
        tests = CodeTest.objects.filter(code=code)
        tests_result = []
        if content and tests and (code.type == Code.EXECUTABLE):
            if code.get_executor_type_id() == Executor.PYTHON36:
                from project.executors.python36.utils import check_tests
                tests_result = check_tests(code, content, tests)
                if code.save_solutions and not request.user.is_anonymous:
                    code_solved = create_or_update_solution(CodeSolution.CHECK_TESTS, request.user, code, content, "", tests_result)

        form = CodeForm(initial={
            "content": content,
            "input": input,
            "output": output,
            "error": error,
        })
        context = {
            "code_solved": code_solved,
            "form": form,
            "code_id": code_id,
            "code_num": request.POST.get("code_num"),
            "show_tests": code.show_tests,
            "show_input": code.show_input,
            "tests": tests,
            "tests_result": tests_result,
        }
        return render(request, code.get_template(), context)
