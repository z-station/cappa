# -*- coding:utf-8 -*-
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponseForbidden
from django.forms import ValidationError
from app.tasks.models import Solution
from app.tasks.forms import ReviewSolutionForm
from app.tasks.services import SolutionService
from app.tasks.filters import SolutionsFilterSet
from app.tasks.services.statistics import UserStatisticsService
from app.common.services.exceptions import ServiceException
from app.common.decorators import teacher_access

UserModel = get_user_model()


@method_decorator(login_required, name='dispatch')
class SolutionView(View):

    def get_object(self) -> Solution:
        pk = self.kwargs['pk']
        if self.request.user.is_teacher:
            return get_object_or_404(Solution, pk=pk)
        else:
            return get_object_or_404(Solution, pk=pk, user=self.request.user)

    def get(self, request, *args, **kwargs):
        solution = self.get_object()
        return render(
            request,
            template_name='tasks/solution/template.html',
            context={
                'object': solution,
                'form': (
                    ReviewSolutionForm(instance=solution)
                    if request.user.is_teacher else None
                )
            }
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return HttpResponseForbidden()
        solution = self.get_object()
        form = ReviewSolutionForm(
            instance=solution,
            data=request.POST
        )
        if form.is_valid():
            try:
                solution = SolutionService.review(
                    reviewer=request.user,
                    solution=solution,
                    **form.cleaned_data
                )
            except ServiceException as ex:
                form.add_error(
                    field=None,
                    error=ValidationError(ex.message, code='invalid')
                )
            else:
                UserStatisticsService.update_course_statistics(
                    user_id=solution.user_id,
                    course_id=solution.type_id
                )

        return render(
            request,
            template_name='tasks/solution/template.html',
            context={
                'object': solution,
                'form': form
            }
        )


@method_decorator(login_required, name='dispatch')
class SolutionsView(View):

    def get_queryset(self):
        return Solution.objects.by_user(self.request.user.id)

    def get_filtered_queryset(self):
        qst = self.get_queryset()
        filterset = SolutionsFilterSet(
            data=self.request.GET,
            queryset=qst,
            request=self.request
        )
        if filterset.is_valid():
            return filterset.filter_queryset(qst)
        else:
            raise Http404

    def get(self, request, *args, **kwargs):
        solutions = list(self.get_filtered_queryset())
        return render(
            request,
            template_name='tasks/solutions/template.html',
            context={
                'solutions': solutions,
            }
        )


@method_decorator(teacher_access, name='dispatch')
class SolutionsDiffView(View):

    def get_object(self) -> Solution:
        pk = self.kwargs['pk']
        return get_object_or_404(Solution, pk=pk)

    def get_pair_solution(self) -> Solution:
        pk = self.kwargs['pair']
        return get_object_or_404(Solution, pk=pk)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name='tasks/solution/diff.html',
            context={
                'object': self.get_object(),
                'pair': self.get_pair_solution(),
            }
        )
