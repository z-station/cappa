from django.shortcuts import render
from django.http import HttpResponse


def groups(request):
    return HttpResponse("groups")
