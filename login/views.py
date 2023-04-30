from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout


from .forms import LoginForm, RegisterForm

#測試
def hello(request):
    return HttpResponse("world")

def testuser(request):
    if request.user.is_authenticated:
        return True
    else:
        return False
    

#首頁
def data(request):

    if request.user.is_authenticated:
        print("已登入")
        name = request.user.username
        email = request.user.email
    else:
        print("未登入")
        name = None
        email = None
        
    now = timezone.now()
    context = {
        'title': '123',
        'heading': name ,
        'content': email,
        'now': now
    }
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
    return render(request, 'registration/register.html', context)


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
    print("登入")
    return render(request, 'registration/login.html', context)

#登出
def log_out(request):
    logout(request)
    print("已登出")
    return redirect('/user/login') #重新導向到登入畫面
