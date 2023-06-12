from django import forms


class TaskBookForm(forms.Form):
    min_rate = forms.CharField(label='мин граница', max_length=3)
    max_rate = forms.CharField(label='макс граница', max_length=3)
    # TODO
    #  difficult = forms. поле с выбором нескольких значений
    #  метки так же
