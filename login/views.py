from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm,UserProfileForm
# from social_django import models as social_models
from .models import UserProfile
from django.contrib.auth.models import User

#測試
def hello(request):
    return HttpResponse("world")


def check_login(request):
    if 'isLogin' in request.session:
        return JsonResponse({'isLogin': request.session['isLogin']})
    else:
        return JsonResponse({'isLogin': False})

# 首頁
def data(request):
    if request.user.is_authenticated:
        print("已登入")
        request.session['isLogin'] = True
        name = request.user.username
        email = request.user.email
    else:
        request.session['isLogin'] = False
        print("未登入")
        name = None
        email = None
        
    now = timezone.now()
    context = {
        'heading': name ,
        'content': email,
        'now': now
    }
    request.session.save() 
    return render(request, 'home123.html', context)

#註冊
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("註冊成功")
            return redirect('/user/login/')  #重新導向到登入畫面
        print("註冊錯誤")
    context = {
        'form': form
    }
    return render(request, 'registration/reg.html', context)


#登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("成功登入")
            return redirect('/user/data/')  #重新導向到首頁
        print("登入錯誤")
    context = {
        'form': form
    }
    # print("登入")
    return render(request, 'registration/login.html', context)

#登出
def log_out(request):
    logout(request)
    request.session['isLogin'] = False
    request.session.save() 
    print(request.session.get('isLogin'))
    print("已登出")
    return redirect('/user/login') #重新導向到登入畫面

#個人資料
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(mail=request.user.email)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('/user/data')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'test456.html', {'form': form})