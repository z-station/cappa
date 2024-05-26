from django.forms import CheckboxSelectMultiple


class CheckboxMultiple(CheckboxSelectMultiple):

    template_name = 'common/widgets/checkbox.html'
    option_template_name = 'common/widgets/checkbox_option.html'
