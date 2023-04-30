from django.http import JsonResponse
from django.shortcuts import render
import requests

# Create your views here.


def iRiver(request):
    url = 'http://127.0.0.1:8000/login/test/'
    response = requests.get(url)
    print(response)
    return render(request, 'index.html')


def setting(requset):
    return render(requset, 'setting.html')


def problem(requset):
    return render(requset, 'problem.html')


def plan(request):
    return render(request, 'plan.html')
