from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def iRiver(request):
    return render(request, 'index.html')


def setting(requset):
    return render(requset, 'setting.html')


def problem(requset):
    return render(requset, 'problem.html')


def plan(request):
    return render(request, 'plan.html')
