from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from django.utils import timezone
from app.training.models import Solution, TaskItem
from app.translators.main import testing
from app.translators.entities.response import (
    ERROR,
    WARNING,
    OK,
    OperationResponse,
    SandboxResponseData
)


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
    translator = forms.IntegerField(widget=forms.HiddenInput)

    def perform_operation(self, user: User, taskitem: TaskItem):
        if self.is_valid():
            operation = getattr(self.Operations, self.cleaned_data['operation'])
            return operation(editor_data=self.cleaned_data, taskitem=taskitem, user=user)
        else:
            return OperationResponse(
                status=ERROR,
                msg='Некорректные данные формы'
            )

    class Operations:

        CHOICES = (
            ('check_tests', 'check_tests'),
            ('save_solution', 'save_solution'),
            ('save_last_changes', 'save_last_changes'),
        )

        @classmethod
        def check_tests(cls, editor_data: dict, taskitem: TaskItem, **kwargs):

            """ Прогнать код по тестам задачи и вернуть результаты тестирования """

            if not taskitem.task.tests:
                return OperationResponse(status=WARNING, msg='Тесты отсутствуют')
            if not taskitem.compiler_check:
                return OperationResponse(status=WARNING, msg='Операция запрещена')
            sandbox_data: SandboxResponseData = testing(
                code=editor_data['content'],
                taskitem=taskitem,
            )
            # Запрос в песочницу прошел успешно
            if sandbox_data['ok']:
                # Тесты пройдены
                if sandbox_data['data']['ok']:
                    return OperationResponse(
                        status=OK,
                        msg='Тесты пройдены',
                        sandbox_data=sandbox_data
                    )
                else:
                    return OperationResponse(
                        status=WARNING,
                        msg='Тесты не пройдены',
                        sandbox_data=sandbox_data
                    )
            else:
                # Запрос к песочнице завершился с ошибкой
                return OperationResponse(
                    status=ERROR,
                    msg=sandbox_data['error']['msg'],
                    sandbox_data=sandbox_data
                )

        @classmethod
        def save_last_changes(cls, editor_data: dict, taskitem: TaskItem, user: User):
            if not user.is_active:
                return OperationResponse(
                    status=WARNING,
                    msg='Требуется авторизация'
                )
            solution, created = Solution.objects.get_or_create(
                user=user, taskitem=taskitem, defaults={
                    "last_changes": editor_data['content']
                })
            if not created:
                solution.last_changes = editor_data['content']
                solution.save()
            return OperationResponse(
                status=OK,
                msg='Сохранено'
            )

        @classmethod
        def save_solution(cls, editor_data: dict, taskitem: TaskItem, user: User):
            return cls.save_last_changes(editor_data, taskitem, user)

        @classmethod
        def ready_solution(cls, editor_data: dict, taskitem: TaskItem, user: User):
            if not user.is_active:
                return OperationResponse(
                    status=WARNING,
                    msg='Требуется авторизация'
                )
            if not editor_data['content']:
                return OperationResponse(
                    status=WARNING,
                    msg='Решение отсутствует'
                )
            solution = Solution.objects.filter(user=user, taskitem=taskitem).first()
            # если у задачи одна попытка и она уже использована - решение нельзя изменить
            if solution and taskitem.one_try and solution.is_locked:
                return OperationResponse(
                    status=WARNING,
                    msg='Решение более нельзя изменить'
                )
            # если задача с автотестами - прогнать автотесты
            tests_score = None
            if taskitem.compiler_check and taskitem.task.tests:
                sandbox_data: SandboxResponseData = testing(
                    code=editor_data['content'],
                    taskitem=taskitem,
                )
                # Запрос в песочницу прошел успешно
                if sandbox_data['ok']:
                    # Тесты пройдены
                    tests_score = (
                        round(
                            sandbox_data['data']['num_ok'] /
                            sandbox_data['data']['num'] * taskitem.max_score,
                            2
                        )
                    )
                else:
                    # Запрос к песочнице завершился с ошибкой
                    return OperationResponse(
                        status=ERROR,
                        msg=sandbox_data.get(
                            'error_msg',
                            'Транслятор кода недоступен (500)'
                        )
                    )
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
            return OperationResponse(
                status=OK,
                msg='Решение отправлено'
            )


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
