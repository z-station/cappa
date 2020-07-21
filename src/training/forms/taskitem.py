from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from django.utils import timezone
from src.training.models import Solution, TaskItem
from .utils import Response


class TaskItemAdminForm(forms.ModelForm):

    class Meta:
        model = TaskItem
        fields = '__all__'

    def clean(self):
        compiler_check = self.cleaned_data.get('compiler_check')
        manual_check = self.cleaned_data.get('manual_check')
        if not manual_check and not compiler_check:
            raise forms.ValidationError('Включите ручную проверку или проверку автотестами')


class TaskItemForm(forms.Form):

    input = forms.CharField(label="Консольный ввод", required=False)
    content = forms.CharField(label='Редактор')
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

    def perform_operation(self, user: User, taskitem: TaskItem):
        if self.is_valid():
            operation = getattr(self.Operations, self.cleaned_data['operation'])
            return operation(editor_data=self.cleaned_data, taskitem=taskitem, user=user)
        else:
            return Response(status=401, msg='Некорректные данные формы')

    class Operations:

        CHOICES = (
            ('debug', 'debug'),
            ('check_tests', 'check_tests'),
            ('create_version', 'create_version'),
            ('save_solution', 'save_solution'),
            ('save_last_changes', 'save_last_changes'),
        )

        @classmethod
        def debug(cls, editor_data: dict, taskitem: TaskItem, **kwargs):
            if not taskitem.compiler_check:
                return Response(status=404, msg='Операция запрещена')
            result = taskitem.lang.provider.debug(
                input=editor_data.get('input', ''),
                content=editor_data['content']
            )
            if result['error']:
                return Response(status=400, msg='Ошибка отладки', output=result['output'], error=result['error'])
            else:
                return Response(status=200, msg='Готово', output=result['output'])

        @classmethod
        def check_tests(cls, editor_data: dict, taskitem: TaskItem, user: User):
            if not taskitem.task.tests:
                return Response(status=300, msg='Тесты отсутствуют')
            if not taskitem.compiler_check:
                return Response(status=404, msg='Операция запрещена')
            tests_result = taskitem.lang.provider.check_tests(
                content=editor_data['content'],
                task=taskitem.task,
            )
            if tests_result['success']:
                return Response(status=200, msg='Тесты пройдены', tests_result=tests_result)
            else:
                return Response(status=300, msg='Тесты не пройдены', tests_result=tests_result)

        @classmethod
        def create_version(cls, editor_data: dict, taskitem: TaskItem, user: User):
            if user.is_active:
                solution, _ = Solution.objects.get_or_create(user=user, taskitem=taskitem)
                solution.create_version(content=editor_data['content'])
                solution.save()
                return Response(status=200, msg='Версия сохранена')
            else:
                return Response(status=402, msg='Требуется авторизация')

        @classmethod
        def save_last_changes(cls, editor_data: dict, taskitem: TaskItem, user: User):
            if not user.is_active:
                return Response(status=402, msg='Требуется авторизация')
            solution, created = Solution.objects.get_or_create(
                user=user, taskitem=taskitem, defaults={
                    "last_changes": editor_data['content']
                })
            if not created:
                solution.last_changes = editor_data['content']
                solution.save()
            return Response(status=200, msg='Изменения сохранены')

        @classmethod
        def save_solution(cls, editor_data: dict, taskitem: TaskItem, user: User):
            return cls.save_last_changes(editor_data, taskitem, user)

        @classmethod
        def ready_solution(cls, editor_data: dict, taskitem: TaskItem, user: User):
            if not user.is_active:
                return Response(status=402, msg='Требуется авторизация')
            if not editor_data['content']:
                return Response(status=404, msg='Решение отсутствует')
            solution = Solution.objects.filter(user=user, taskitem=taskitem).first()
            # если у задачи одна попытка и она уже использована - решение нельзя изменить
            if solution and taskitem.one_try and solution.is_locked:
                return Response(status=403, msg='Операция запрещена')
            # если задача с автотестами - прогнать автотесты
            tests_score = None
            if taskitem.compiler_check and taskitem.task.tests:
                tests_result = taskitem.lang.provider.check_tests(
                    content=editor_data['content'],
                    task=taskitem.task,
                )
                tests_score = round(tests_result['num_success'] / tests_result['num'] * taskitem.max_score, 2)
            if solution is None:
                solution = Solution(user=user, taskitem=taskitem)
            solution.tests_score = tests_score
            solution.content = editor_data['content']
            solution.last_changes = editor_data['content']
            solution.is_locked = taskitem.one_try
            solution.last_modified = timezone.now()
            solution.set_is_count()
            if solution.taskitem.manual_check:
                solution.manual_status = Solution.MS__READY_TO_CHECK
            solution.save()
            return Response(status=200, msg='Решение отправлено')


class SolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = ('manual_status', 'manual_score', 'comment')

    manual_status = forms.CharField(
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'}, choices=Solution.MS__CHOICES)
    )
    manual_score = forms.FloatField(
        label='Оценка', required=False,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'})
    )
    comment = forms.CharField(label='Комментарий преподавателя', widget=TinyMCE, required=False)

    def clean(self):
        manual_score = self.cleaned_data.get('manual_score')
        manual_status = self.cleaned_data.get('manual_status')
        # проверка что оценка в диапазоне 0..max_score
        if manual_score is not None:
            max_score = self.instance.taskitem.max_score
            if manual_score < 0 or manual_score > max_score:
                raise forms.ValidationError(f'Оценка должна находиться в диапазоне от 0 до {max_score} баллов')
        # проверка что оценка стоит если статус "проверено"
        if manual_status == Solution.MS__CHECKED and manual_score is None:
            raise forms.ValidationError(f'Вы забыли поставить оценку')


__all__ = ['TaskItemForm', 'SolutionForm', 'TaskItemAdminForm']
