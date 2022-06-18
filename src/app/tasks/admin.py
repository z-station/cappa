from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    RelatedDropdownFilter,
    ChoiceDropdownFilter
)
from app.tasks.models import (
    Task,
    Tag,
    SolutionExample,
    Source,
    Solution,
    ExternalSolution
)
from app.tasks.enums import (
    SolutionType,
    ScoreMethod
)
from app.tasks.forms import (
    TaskAdminForm,
    SolutionAdminForm,
    SolutionExampleAdminForm,
    ExternalSolutionAdminForm,
)
from app.translators.enums import TranslatorType


class SolutionExampleInline(admin.StackedInline):

    model = SolutionExample
    form = SolutionExampleAdminForm
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('admin/tasks/style.css',)}
        js = (
            'django_tinymce/jquery-1.9.1.min.js',
            'admin/tasks/jsoneditor.min.js',
            'js/ace-1.4.7/ace.js',
            'admin/ace_init.js',
            'admin/tasks/task.js'
        )

    model = Task
    form = TaskAdminForm
    exclude = ('order_key',)
    raw_id_fields = ("author",)
    search_fields = ('title',)
    list_display = ('title',)
    filter_horizontal = ('tags',)
    inlines = (SolutionExampleInline,)
    list_filter = (
        'output_type',
        ('tags', RelatedDropdownFilter),
        ('difficulty', ChoiceDropdownFilter),
        ('source', RelatedDropdownFilter),
    )


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):

    class Media:
        js = [
            'js/ace-1.4.7/ace.js',
            'admin/ace_init.js',
            'admin/tasks/solution.js',
        ]
        css = {
            'all': ['admin/ace.css']
        }

    model = Solution
    form = SolutionAdminForm

    def get_queryset(self, request):
        qst = super().get_queryset(request)
        return qst.internal()

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_teacher

    def has_delete_permission(self, request, obj=None):
        return request.user.is_teacher

    def user_info(self, obj: Solution) -> str:
        if obj.user_first_name:
            result = f'{obj.user_last_name} {obj.user_first_name} '
            if obj.user_email:
                result += obj.user_email
            elif obj.user_username:
                result += obj.user_username
        else:
            result = '-'
        return result
    user_info.short_description = 'пользователь'

    def user_full_name(self, obj: Solution) -> str:
        result = (
            f'{obj.user_last_name} '
            f'{obj.user_first_name} '
            f'{obj.user_father_name or ""}'
        )
        return result
    user_full_name.short_description = 'пользователь'

    def reviewer_info(self, obj: Solution) -> str:
        if obj.reviewer_first_name:
            return (
                f'{obj.reviewer_last_name} '
                f'{obj.reviewer_first_name} '
                f'{obj.reviewer_father_name or ""}'
            )
        else:
            return ''
    reviewer_info.short_description = 'преподаватель'

    def translator_name(self, obj: Solution):
        return TranslatorType.MAP.get(obj.translator, '-')
    translator_name.short_description = 'язык'

    def score(self, obj: Solution) -> int:
        return obj.review_score or obj.testing_score
    score.short_description = 'оценка'

    def get_type_name(self, obj: Solution) -> str:
        return f'{obj.type_name_value}: {obj.type_name}'
    get_type_name.short_description = 'Источник решения'

    def changeform_view(
        self,
        request,
        object_id=None,
        form_url='',
        extra_context=None
    ):
        """ Отключение кнопок сохранения на странице редактирования """

        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().changeform_view(
            request,
            object_id,
            form_url='',
            extra_context=extra_context
        )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj.score_method == ScoreMethod.TESTS:
            fieldsets[1] = (
                'Результаты тестирования кода', {
                    'fields': (
                        'count_tests',
                        'count_passed_tests',
                        'testing_score',
                    )
                }
            )
        elif obj.score_method == ScoreMethod.REVIEW:
            fieldsets[1] = (
                'Результаты проверки преподавателем', {
                    'fields': (
                        'reviewer_info',
                        'review_status',
                        'review_score',
                        'review_date',
                        'reviewer_comment',
                        'hide_review_score',
                        'hide_reviewer_comment',
                    )
                }
            )
        elif obj.score_method == ScoreMethod.TESTS_AND_REVIEW:
            fieldsets[1] = (
                'Результаты тестирования и проверки', {
                    'fields': (
                        'count_tests',
                        'count_passed_tests',
                        'testing_score',
                        'reviewer_info',
                        'review_status',
                        'review_score',
                        'review_date',
                        'reviewer_comment',
                        'hide_review_score',
                        'hide_reviewer_comment',
                    )
                }
            )

        return fieldsets

    fieldsets = [
        (
            'Общая информация', {
                'fields': (
                    'task_name',
                    'translator_name',
                    'user_info',
                    'created',
                    'max_score',
                    'get_type_name',
                    'score_method'
                )
            }
        ),
        (
            'Заглушка для метода get_fieldsets', {
                'fields': ()
            }
        ),
        (
            'Решение', {
                'fields': (
                    'content',
                )
            }
        )
    ]
    readonly_fields = (
        'user_info',
        'task_name',
        'translator',
        'type',
        'get_type_name',
        'created',
        'max_score',
        'review_date',
        'testing_score',
        'reviewer_info',
        'review_score',
        'review_status',
        'count_tests',
        'count_passed_tests',
        'translator_name',
        'reviewer_comment',
        'hide_review_score',
        'hide_reviewer_comment',
        'score_method',
    )
    list_display = (
        'task_name',
        'user_full_name',
        'created',
        'translator_name',
        'score_method',
        'score',
    )
    search_fields = (
        'user_first_name',
        'user_last_name',
        'user_father_name',
        'task_name'
    )
    list_filter = (
        'translator',
        'score_method',
    )


@admin.register(ExternalSolution)
class ExternalSolutionAdmin(admin.ModelAdmin):

    class Media:
        js = [
            'django_tinymce/jquery-1.9.1.min.js',
            'js/ace-1.4.7/ace.js',
            'admin/tinymce_init.js',
            'admin/ace_init.js',
            'admin/tasks/external_solution.js',
        ]
        css = {
            'all': ['admin/ace.css']
        }

    model = ExternalSolution
    form = ExternalSolutionAdminForm

    def get_queryset(self, request):
        qst = super().get_queryset(request)
        return qst.external()

    def has_add_permission(self, request, obj=None):
        return request.user.is_teacher

    def has_change_permission(self, request, obj=None):
        return request.user.is_teacher

    def has_delete_permission(self, request, obj=None):
        return request.user.is_teacher

    def save_model(self, request, obj, form, change):
        obj.external_source_name = obj.external_source.name
        obj.task_name = obj.task.title
        obj.type = SolutionType.EXTERNAL
        obj.save()

    fieldsets = (
        (
            'Информация о источнике решения', {
                'fields': (
                    'external_source_name',
                    'external_source',
                    'description',
                )
            }
        ),
        (
            'Задача', {
                'fields': (
                    'task_name',
                    'task',
                )
            }
        ),
        (
            'Решение', {
                'fields': (
                    'translator',
                    'content',
                )
            }
        )
    )

    raw_id_fields = (
        'external_source',
        'task',
    )
    readonly_fields = (
        'external_source_name',
        'task_name',
    )


admin.site.register(Tag)
admin.site.register(Source)
