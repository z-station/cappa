# -*- coding:utf-8 -*-

from django.shortcuts import HttpResponse, render, get_object_or_404, Http404
from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, Executor, UserSolution
from project.executors.utils import create_or_update_solution


def execute(request):
    """ Обрабатывает ajax-запросы исполнения блока кода со страницы
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
        tests = CodeTest.objects.filter(code=code)
        code_solved = request.POST.get("code_solved", False)
        if content:
            if code.get_executor_type_id() == Executor.PYTHON36:
                from project.executors.python36.utils import execute_code
                output, error = execute_code(code, content, input)
            elif code.get_executor_type_id() == Executor.CPP:
                from project.executors.cpp.utils import execute_code
                output, error = execute_code(code, content, input)
            elif code.get_executor_type_id() == Executor.CH:
                from project.executors.ch.utils import execute_code
                output, error = execute_code(code, content, input)

        form = CodeForm(initial={
            "content": content,
            "input": input,
            "output": output,
            "error": error,
        })
        context = {
            "code_solved": code_solved,
            "executor_name": code.get_executor_name(),
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
        code_solved = None
        tests = CodeTest.objects.filter(code=code)
        tests_result = []
        if content and tests and (code.type == Code.EXECUTABLE):
            if code.get_executor_type_id() == Executor.PYTHON36:
                from project.executors.python36.utils import check_tests
                tests_result = check_tests(code, content, tests)
                if code.save_solutions and not request.user.is_anonymous:
                    code_solved = create_or_update_solution(request.user, code, tests_result, content)

            elif code.get_executor_type_id() == Executor.CPP:
                from project.executors.cpp.utils import check_tests
                tests_result = check_tests(code, content, tests)
                if code.save_solutions and not request.user.is_anonymous:
                    code_solved = create_or_update_solution(request.user, code, tests_result, content)

            elif code.get_executor_type_id() == Executor.CH:
                from project.executors.ch.utils import check_tests
                tests_result = check_tests(code, content, tests)
                if code.save_solutions and not request.user.is_anonymous:
                    code_solved = create_or_update_solution(request.user, code, tests_result, content)

        form = CodeForm(initial={
            "content": content,
            "input": input,
            "output": output,
            "error": error,
        })
        context = {
            "code_solved": code_solved,
            "executor_name": code.get_executor_name(),
            "form": form,
            "code_id": code_id,
            "code_num": request.POST.get("code_num"),
            "show_tests": code.show_tests,
            "show_input": code.show_input,
            "tests": tests,
            "tests_result": tests_result["data"],
        }
        return render(request, code.get_template(), context)


def user_solution(request, user_id, code_id):
    # Заменить на проверку владельца группы
    if not request.user.is_superuser:
        raise Http404
    user_solution_obj = get_object_or_404(UserSolution, user=user_id, code=code_id)
    solutions = user_solution_obj.details["solutions"]
    if solutions:
        template = user_solution_obj.code.get_template("code_solution.html")
        num = user_solution_obj.details.get("best_solution_num")
        if num is not None:
            solution = user_solution_obj.details["solutions"][num]
            tests = user_solution_obj.details["best_solution_tests"]
        else:
            solution = user_solution_obj.details["solutions"].pop()
            tests = []

        form = CodeForm(initial={
            "content": solution["content"],
            "input": None,
            "output": None,
            "error": None,
        })

        try:
            # TODO сделать замену тега на форму
            treeitem = user_solution_obj.code.treeitem
            title = treeitem.long_title if treeitem.long_title else treeitem.title
            content = treeitem.content

            import re
            code_tag_pattern = re.compile(r'<\w+>[&nbsp;]*#code[0-9]+#[&nbsp;]*</\w+>|[&nbsp;]*#code[0-9]+#[&nbsp;]*')
            content = re.sub(code_tag_pattern, "", content)
        except:
            title = None
            content = None

        executor_name = Code.objects.get(id=code_id).get_executor_name()

        css_class = "process"
        if user_solution_obj.progress == 0:
            css_class = "unluck"
        elif user_solution_obj.progress == 100:
            css_class = "success"
        solution["css_class"] = css_class

        context = {
            "treeitem_title": title,
            "treeitem_content": content,
            "form": form,
            "object": user_solution_obj,
            "solution": solution,
            "tests_result": tests,
            "solution_user": user_solution_obj.user,
            "executor_name": executor_name,
        }
        return render(request, template, context)
    else:
        return Http404
