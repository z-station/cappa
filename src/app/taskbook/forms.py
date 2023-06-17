from django import forms
from app.taskbook.models import TaskBookItem
from app.translators.enums import TranslatorType


class TaskBookForm(forms.Form):
    min_rate = forms.CharField(label='мин граница',
                               max_length=3,
                               required=False)
    max_rate = forms.CharField(label='макс граница',
                               max_length=3,
                               required=False)

    DIFFICULT_CHOICES = [
        ('easy', 'легкая'),
        ('normal', 'нормальная'),
        ('hard', 'сложная'),
        ('legendary', 'легендарная'),
    ]
    difficulties = forms.MultipleChoiceField(label='сложность',
                                             choices=DIFFICULT_CHOICES,
                                             widget=forms.CheckboxSelectMultiple(),
                                             required=False)

    MARK_CHOICES = [
        ('conditions', 'условия'),
        ('cycles', 'циклы'),
    ]
    marks = forms.MultipleChoiceField(label='метки',
                                      choices=MARK_CHOICES,
                                      widget=forms.CheckboxSelectMultiple(),
                                      required=False)

    def clean(self):
        min_rate = self.cleaned_data['min_rate']
        max_rate = self.cleaned_data['max_rate']

        if not min_rate.isnumeric() or not max_rate.isnumeric():
            self.add_error(field='min_rate', error='Рейтинг должен быть числом.')
        elif min_rate > max_rate:
            self.add_error(field='min_rate', error='Нижняя граница не может быть больше верхней.')

        return self.cleaned_data


class TaskBookItemAdminForm(forms.ModelForm):

    class Meta:
        model = TaskBookItem
        fields = '__all__'

    translator = forms.TypedMultipleChoiceField(
        choices=TranslatorType.CHOICES
    )
