# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render, get_object_or_404, Http404
from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, Executor, UserSolution
from django.core.exceptions import PermissionDenied


def render_executor_blocks(content, code_num, executor_name, input='', output='', error='', tests=None, success=False):

    msg, status = '', ''
    block_error, block_output, block_tests = '<div></div>', '<div></div>', '<div></div>'

    block_input = render_to_string(
        'executors/ace/widget.html',
        {'field': {'name': 'input', 'label': 'Ввод', 'value': input}, 'code_num': code_num, 'executor_name': executor_name}
    )

    block_content = render_to_string(
        'executors/ace/widget.html',
        {'field': {'name': 'content', 'label': '', 'value': content}, 'code_num': code_num, 'executor_name': executor_name}
    )

    if tests:
        block_tests = render_to_string('executors/ace/tests_results.html', {'tests': tests})
        msg, status = 'Пройдено тестов: %s из %s' % (tests['success_num'], tests['num']), 'success'

    elif error:
        block_error = render_to_string(
            'executors/ace/widget.html',
            {'field': {'name': 'error', 'label': 'Ошибка', 'value': error}, 'code_num': code_num, 'executor_name': executor_name}
        )
        msg, status = 'Ошибка', 'warning'

    elif output:
        block_output = render_to_string(
            'executors/ace/widget.html',
            {'field': {'name': 'output', 'label': 'Вывод', 'value': output}, 'code_num': code_num, 'executor_name': executor_name}
        )
    if not error:
        msg, status = 'Готово', 'success'

    return {
        'input': block_input,
        'content': block_content,
        'output': block_output,
        'error': block_error,
        'msg': msg,
        'status': status,
        'tests': block_tests,
        'success': success,
    }


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
        # code_solved = request.POST.get("code_solved", False)
        if content:
            output, error = code.execute(content, input)
        return JsonResponse(
            render_executor_blocks(
                content=content,
                code_num=request.POST.get("code_num"),
                executor_name=code.get_executor_name(),
                input=input,
                output=output,
                error=error,
            )
        )


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
        tests = CodeTest.objects.filter(code=code)
        success = False
        if content and tests and (code.type == Code.EXECUTABLE):
            tests_result = code.check_tests(content, input, tests)
            if code.save_solutions and not request.user.is_anonymous:
                user_solution, _ = UserSolution.objects.get_or_create(user=request.user, code=code)
                user_solution.update_best(data=tests_result)
                user_solution.save()
                success = user_solution.status_success

        return JsonResponse(
            render_executor_blocks(
                content=content,
                code_num=request.POST.get("code_num"),
                executor_name=code.get_executor_name(),
                input=input,
                output=output,
                error=error,
                tests=tests_result,
                success=success
            )
        )

def save_version(request):

    try:
        code_id = request.POST.get("code_id")
        code = Code.objects.get(id=code_id)
    except Code.DoesNotExist:
        return HttpResponse("Code does not exist")
    else:
        content = request.POST.get("content")
        input, error = request.POST.get("input", ""), ""
        msg, status = '', ''
        tests = CodeTest.objects.filter(code=code)
        if content and tests and (code.type == Code.EXECUTABLE):
            tests_result = code.check_tests(content, input, tests)
            if code.save_solutions and not request.user.is_anonymous:
                user_solution, _ = UserSolution.objects.get_or_create(user=request.user, code=code)
                user_solution.add_version(data=tests_result)
                user_solution.save()
                status = 'success'
                msg = 'Версия сохранена'

    return JsonResponse({
        'status': status,
        'msg': msg
    })


def user_solution(request, user_id, code_id):

    user_solution = get_object_or_404(UserSolution, user=user_id, code=code_id)
    if user_solution.progress is None:
        raise Http404
    if not(request.user == user_solution.user or request.user.is_superuser):
        raise PermissionDenied
    else:
        template = "executors/code_solution.html"
        form = CodeForm(initial={
            "content": user_solution.best["content"],
            "input": user_solution.best["input"],
            "output": None,
            "error": None,
        })

        treeitem = user_solution.code.treeitem

        context = {
            "form": form,
            "object": treeitem,
            "solution": user_solution,
            "executor_name": user_solution.code.get_executor_name(),
            "disabled": True,
            "code_num": user_solution.code.id
        }
        return render(request, template, context)
