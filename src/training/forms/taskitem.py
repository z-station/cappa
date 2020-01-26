from django import forms
from src.training.models import Solution
from .utils import Response


class TaskItemForm(forms.Form):

    input = forms.CharField(label="Ввод", required=False)
    content = forms.CharField(label='')
    output = forms.CharField(
        label="Вывод", required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    error = forms.CharField(
        label="Ошибка", required=False,
        widget=forms.Textarea(attrs={'readonly': True})
    )
    operation = forms.CharField(widget=forms.Select(choices='Operations.CHOICES'))
    lang = forms.CharField(widget=forms.HiddenInput)

    def perform_operation(self, user, taskitem):
        if self.is_valid():
            return getattr(self.Operations, self.cleaned_data['operation'])(self.cleaned_data, taskitem, user)
        else:
            return Response(msg='Некорректные данные формы', status='203')

    class Operations:

        CHOICES = (
            ('debug', 'debug'),
            ('tests', 'tests'),
            ('create_version', 'create_version'),
            ('save_last_changes', 'save_last_changes'),
        )

        @staticmethod
        def debug(data, taskitem, user):
            result = taskitem.lang.debug(data['input'], data['content'])
            if result['error']:
                return Response(202, 'Ошибка отладки', output=result['output'], error=result['error'])
            else:
                return Response(200, 'Готово', output=result['output'])

        @staticmethod
        def tests(data, taskitem, user):
            tests_result = taskitem.lang.tests(data['content'], taskitem.task.tests)
            if user.is_active:
                solution, _ = Solution.objects.get_or_create(user=user, taskitem=taskitem)
                solution.update(data['content'], tests_result)
                solution.save()
                tests_result['status'] = solution.status
                tests_result['id'] = 'taskitem__%d' % taskitem.id

            if tests_result['success']:
                return Response(200, 'Тесты пройдены', tests_result=tests_result)
            else:
                return Response(201, 'Тесты не пройдены', tests_result=tests_result)

        @staticmethod
        def create_version(data, taskitem, user):
            if user.is_active:
                tests_result = taskitem.lang.tests(data['content'], taskitem.task.tests)
                solution, _ = Solution.objects.get_or_create(user=user, taskitem=taskitem)
                solution.create_version(data['content'], tests_result)
                solution.save()
                return Response(200, 'Версия сохранена')
            else:
                return Response(204, 'Требуется авторизация')

        @staticmethod
        def save_last_changes(data, taskitem, user):
            if user.is_active:
                solution, _ = Solution.objects.get_or_create(user=user, taskitem=taskitem)
                solution.last_changes = data['content']
                solution.save()
                return Response(200, 'Изменения сохранены')
            else:
                return Response(204, 'Требуется авторизация')


__all__ = ['TaskItemForm']
