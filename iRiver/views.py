from django.http import JsonResponse
from django.shortcuts import render
import requests
import json
from django.shortcuts import redirect, render

# Create your views here.


def iRiver(request):
    url = 'http://127.0.0.1:8000/user/test/'
    csrftoken = request.COOKIES.get('csrftoken')
    session_id = request.COOKIES.get('sessionid')
    headers = {'Cookie': f'csrftoken={csrftoken}; sessionid={session_id};'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(result['isLogin'])
        if result['isLogin']:
            return render(request, 'index.html')
        else:
            return redirect('/user/login/')
    else:
        # 请求失败
        print(f'Request failed with status code {response.status_code}')
        return render(request, 'index.html')


def setting(requset):
    return render(requset, 'setting.html')


def problem(requset):
    return render(requset, 'problem.html')


def plan(request):
    return render(request, 'plan.html')
