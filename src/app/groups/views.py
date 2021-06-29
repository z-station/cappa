from django.shortcuts import render, Http404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from app.groups.models import Group, GroupCourse, GroupMember
from app.groups.forms import GroupSearchForm, GroupInviteForm


class GroupListView(View):

    def get(self, request, *args, **kwargs):
        objects = Group.objects.filter(show=True).prefetch_related('_members')
        search = request.GET.get('search')
        form = GroupSearchForm(data=request.GET)
        if search:
            objects = objects.filter(title__icontains=search)

        return render(
            template_name='groups/groups_list.html',
            context={
                'objects': objects,
                'form': form
            },
            request=request
        )


class GroupView(View):

    def get_object(self,  *args, **kwargs):
        try:
            return Group.objects.prefetch_related('_members').get(
                id=kwargs['group_id'])
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):

        group = self.get_object(*args, **kwargs)
        form = None
        if request.user.is_active:
            if request.user not in group.members:
                form = GroupInviteForm(instance=group)
        return render(
            template_name='groups/group.html',
            context={
                'object': group,
                'form': form,
                'user_is_member': request.user in group.members,
                'user_is_teacher': request.user == group.author,
            },
            request=request
        )

    def post(self, request, *args, **kwargs):
        if request.user.is_active:
            group = self.get_object(*args, **kwargs)
            form = GroupInviteForm(instance=group, data=request.POST)
            user_is_member = request.user in group.members
            if not user_is_member:
                if form.is_valid():
                    GroupMember.objects.create(group=group, user=request.user)
                    user_is_member = True
                    form = None
                return render(
                    template_name='groups/group.html',
                    context={
                        'object': group,
                        'form': form,
                        'user_is_member': user_is_member
                    },
                    request=request
                )
            return redirect(reverse('groups:group', kwargs={'group_id': group.id}))

        raise Http404


@method_decorator(login_required, name='dispatch')
class GroupCourseView(View):

    def get_object(self, *args, **kwargs):
        try:
            group_course = GroupCourse.objects.select_related('group', 'course').get(id=kwargs['group_course_id'])
        except:
            raise Http404
        else:
            if not group_course.show_table:
                raise Http404
            return group_course

    def get(self, request, *args, **kwargs):
        group_course = self.get_object(*args, **kwargs)
        group = group_course.group
        if(request.user == group.author or request.user in group.members):
            return render(
                request=request,
                template_name='groups/group_course.html',
                context={
                    'object': group_course,
                    'course_data': group_course.course.get_cache_data()
                }
            )
        else:
            raise Http404


@method_decorator(login_required, name='dispatch')
class GroupCourseSolutionsView(View):

    def get_object(self, *args, **kwargs):
        try:
            group_course = GroupCourse.objects.select_related('group', 'course').get(id=kwargs['group_course_id'])
        except:
            raise Http404
        else:
            if not group_course.show_table:
                raise Http404
            return group_course

    def get(self, request, *args, **kwargs):
        group_course = self.get_object(request, *args, **kwargs)
        group = group_course.group
        course = group_course.course
        result = {}
        for user in group.members:
            result['member-%d' % user.id] = {
                'full_name': user.get_full_name(),
                'data': user.get_cache_course_solutions_data(course),
                'show_link': request.user.is_superuser or
                             request.user == user or
                             request.user == group.author
            }
        return JsonResponse(result)
