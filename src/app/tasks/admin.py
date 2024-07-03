from django.contrib import admin
from django.db import transaction
from django.utils.encoding import force_text
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
    ExternalSolution,
    Checker,
)
from app.tasks.enums import (
    TaskItemType,
    ScoreMethod
)
from app.tasks.forms import (
    TaskAdminForm,
    SolutionAdminForm,
    SolutionExampleAdminForm,
    ExternalSolutionAdminForm,
    CheckerAdminForm,
)
from app.translators.enums import TranslatorType
from app.tasks.services.statistics import UserStatisticsService
from app.common.admin.mixins import DeleteSelectedMixin


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
            'admin/tasks/jsoneditor1.min.js',
            'js/ace-1.4.7/ace.js',
            'admin/ace_init.js',
            'admin/tasks/task1.js'
        )

    model = Task
    form = TaskAdminForm
    readonly_fields = (
        'rating',
        'rating_total',
        'rating_success',
    )
    exclude = ('order_key',)
    raw_id_fields = ("author",)
    search_fields = ('title',)
    list_display = ('title',)
    filter_horizontal = ('tags',)
    inlines = (SolutionExampleInline,)
    list_filter = (
        'testing_checker',
        ('tags', RelatedDropdownFilter),
        ('difficulty', ChoiceDropdownFilter),
        ('source', RelatedDropdownFilter),
    )


@admin.register(Solution)
class SolutionAdmin(
    DeleteSelectedMixin,
    admin.ModelAdmin
):

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

    def get_type_name(self, obj: Solution) -> str:
        if obj.type_course:
            return f'{obj.type_name_value}: {obj.type_name}'
        else:
            return obj.type_name_value
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
                    'score_method',
                    'score'
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
        'score'
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

    @staticmethod
    def perform_delete_selected(modeladmin, request, queryset):

        """ When delete multiple solutions - delete course statistics
            for each course and user """

        """ Perform delete many records """

        pairs = set()
        for obj in queryset:
            obj_display = force_text(obj)
            modeladmin.log_deletion(request, obj, obj_display)
            if obj.type == TaskItemType.COURSE:
                pairs.add((obj.type_id, obj.user_id))

        with transaction.atomic():
            queryset.delete()
            for (course_id, user_id) in pairs:
                UserStatisticsService.delete_course_statistics(
                    course_id=course_id,
                    user_id=user_id
                )

    def delete_model(self, request, obj: Solution):

        """ When delete solution - delete course statistics """

        with transaction.atomic():
            if obj.type == TaskItemType.COURSE and obj.user:
                UserStatisticsService.delete_course_statistics(
                    course_id=obj.type_id,
                    user_id=obj.user.id
                )
            obj.delete()


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
        obj.type = TaskItemType.EXTERNAL
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


@admin.register(Checker)
class CheckerAdmin(admin.ModelAdmin):

    class Media:
        js = [
            'django_tinymce/jquery-1.9.1.min.js',
            'js/ace-1.4.7/ace.js',
            'admin/ace_init.js',
            'admin/tasks/checker.js'
        ]
        css = {
            'all': [
                'admin/ace.css'
            ]
        }

    model = Checker
    form = CheckerAdminForm


admin.site.register(Tag)
admin.site.register(Source)
