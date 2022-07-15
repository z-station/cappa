from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from app.groups.models import (
    Group,
    GroupMember,
    GroupCourse
)
from app.groups.forms import GroupSearchForm, GroupInviteForm
from app.translators.enums import TranslatorType


class GroupListView(View):

    def get_queryset(self):
        user = self.request.user
        user_id = user.id if user.is_authenticated else None
        search = self.request.GET.get('search')
        qst = Group.objects.active().with_learners_count(
        ).with_user_is_learner(
            user_id
        ).with_user_is_teacher(
            user_id
        )
        if search:
            qst = qst.filter(title__icontains=search)
        return qst

    def get(self, request, *args, **kwargs):

        return render(
            template_name='groups/groups_list.html',
            context={
                'groups': self.get_queryset(),
                'form': GroupSearchForm(data=request.GET)
            },
            request=request
        )


class GroupView(View):

    def get_queryset(self):
        user = self.request.user
        user_id = user.id if user.is_authenticated else None
        return Group.objects.active().with_user_is_learner(
            user_id
        ).with_user_is_teacher(
            user_id
        ).prefetch_related('members', 'group_courses')

    def get_object(self):
        group_id = self.kwargs['group_id']
        qst = self.get_queryset()
        try:
            return qst.get(id=group_id)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):

        group = self.get_object()
        if group.user_is_learner or group.user_is_teacher:
            form = None
        else:
            form = GroupInviteForm(instance=group)
        return render(
            template_name='groups/group.html',
            context={
                'object': group,
                'form': form,
                'translators_antiplag_allowed': TranslatorType.ANTIPLAG_ALLOWED
            },
            request=request
        )

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        group = self.get_object()
        form = GroupInviteForm(instance=group, data=request.POST)
        if form.is_valid():
            GroupMember.objects.create(group=group, user=request.user)
            group.user_is_learner = True
            form = None
        return render(
            template_name='groups/group.html',
            context={
                'object': group,
                'form': form,
            },
            request=request
        )


@method_decorator(login_required, name='dispatch')
class GroupCourseStatisticsView(View):

    def get_object(self, *args, **kwargs):
        try:
            course_id = int(self.request.GET['course_id'])
            group_id = kwargs['group_id']
            group_course = GroupCourse.objects.select_related(
                'group',
                'course'
            ).get(
                group_id=group_id,
                group__is_active=True,
                course_id=course_id
            )
        except (ObjectDoesNotExist, TypeError, IndexError):
            raise Http404
        else:
            return group_course

    def get(self, request, *args, **kwargs):
        group_course = self.get_object(*args, **kwargs)
        if request.user:
            return render(
                request=request,
                template_name='groups/group_course.html',
                context={
                    'object': group_course,
                    'group': group_course.group,
                    'course': group_course.course,
                    'course_data': group_course.course.get_cache_data()
                }
            )
        else:
            raise Http404


@method_decorator(login_required, name='dispatch')
class GroupCoursePlagStatisticsView(View):

    def get_object(self, *args, **kwargs):
        try:
            course_id = int(self.request.GET['course_id'])
            group_id = kwargs['group_id']
            group_course = GroupCourse.objects.select_related(
                'group',
                'course'
            ).get(
                group_id=group_id,
                group__is_active=True,
                course_id=course_id
            )
        except (ObjectDoesNotExist, TypeError, IndexError):
            raise Http404
        else:
            return group_course

    def get(self, request, *args, **kwargs):
        group_course = self.get_object(*args, **kwargs)
        if group_course.course.translator in TranslatorType.ANTIPLAG_ALLOWED:
            return render(
                request=request,
                template_name='groups/group_antiplag.html',
                context={
                    'object': group_course,
                    'group': group_course.group,
                    'course': group_course.course,
                    'course_data': group_course.course.get_cache_data()
                }
            )
        else:
            raise Http404
