from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm,UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
import json
# line

# 自製
import user.lib.sql.config
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.sql.sql_music_list import SQL as SQL_music_list

#測試
# def get_user_data(request):

def get_user_music_list(request):
    sql_user_music_list = SQL_music_list(user.lib.sql.config.DB_CONFIG_user_music_list,table_name= (request.session['email']).split("@")[0])
    sql_user_music_list.create_tables()
    if request.method != 'POST':
        return HttpResponse('error')
    # 解析 JSON 数据
    data = json.loads(request.body)
    method = data.get('method')
    if method == 'insert':
        return JsonResponse(json.dumps({'success': sql_user_music_list.save_data(music_ID_list= json.dumps([data.get('music_ID')],indent=4) , music_list= data.get('music_list' , 1),)}), safe=False)
    elif method == 'get':
        return JsonResponse(list(sql_user_music_list.get_music_list(music_list= data.get('music_list' , 1))), safe=False)
    elif method == 'delete':
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_data(music_ID_list= json.dumps([data.get('music_ID')] , indent=4) , music_list=  data.get('music_list' , 1))}), safe=False)
    elif method == 'favorite':
        return JsonResponse(json.dumps({'success': sql_user_music_list.setfavorite(music_ID_list= json.dumps([data.get('music_ID')] , indent=4))}), safe=False)


def hello(request):
    temp = request.session['email']
    mail = temp.split("@")[0]

    key = mail
    
    sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
    sql_user.create_tables(table_name= key)

    sql_user_music_list = SQL_music_list(user.lib.sql.config.DB_CONFIG_user_music_list,table_name= key)
    sql_user_music_list.create_tables()

    music_ID_dict = {
        '111',
        '222',
    }
    music_ID_list = [music for music in music_ID_dict]
    #sql_user_music_list.save_data(music_ID_list= json.dumps( music_ID_list , indent=4))
    #sql_user_music_list.delete_data(music_ID_list= json.dumps( music_ID_list , indent=4))

    #查詢結果
    music_ID_list = sql_user_music_list.get_music_list()
    #return json.dumps(music_ID_list, indent=4)
    
    return HttpResponse(music_ID_list)


def check_login(request):
    if 'isLogin' in request.session:
        return JsonResponse({'isLogin': request.session['isLogin']})
    else:
        return JsonResponse({'isLogin': False})

# 首頁
def data(request):
    if request.user.is_authenticated:
        print("已登入")
        user = request.user
        social = UserSocialAuth.objects.get(provider='line', user=user)
        extra_data = social.extra_data
        if(extra_data.get('email')):
            email = extra_data.get('email')
            print(email)

        else:
            email = request.user.email
        name = request.user.username
        request.session['isLogin'] = True
        request.session['email'] = email
    else:
        del request.session['email']
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
        else:
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
        else:
            print("登入錯誤")
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)

#登出
def log_out(request):
    logout(request)
    request.session['isLogin'] = False
    request.session.save() 
    print(request.session.get('isLogin'))
    print("已登出")
    return redirect('/user/login') 

#個人資料
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(email=request.session['email'])
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            user_data = form.cleaned_data
            sql = SQL_user(user.lib.sql.config.DB_CONFIG_user)
            sql.create_tables("user") #建立資料表            
            sql.save_user_data(**user_data)
            print("成功修改")
            return redirect('/user/data')
    else:
        print("修改錯誤")
        form = UserProfileForm(instance=user_profile)
    return render(request, 'test456.html', {'form': form})

#line

 