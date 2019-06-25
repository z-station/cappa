# -*- coding:utf-8 -*-

from django.conf.urls import url

from project.profile.views import profile

app_name = 'modules'
urlpatterns = [
    url(r'^$', profile, name=''),
]

"""
    /profile/
    /profile/settings/
    /profile/groups/
    /profile/groups/group_id/
    /profile/events/
    /profile/events/event_id/
    /profile/solutions/solution_id/ - мои решения
"""
