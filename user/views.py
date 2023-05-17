from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import LoginForm
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
import json
# 自製
import user.lib.sql.config
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.switch_key import switch_key


def save_session(request):
    sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
    
    user_data = sql_user.get_user_data(switch_key(request.session['email']))
    request.session['user_data'] = user_data

    sql_user_music_list = SQL_music_list(config= user.lib.sql.config.DB_CONFIG_user_music_list, table_name= switch_key(request.session['email']))
    sql_user_music_list.create_tables()
    user_playlist = sql_user_music_list.get_playlists(isAll= True);
    request.session['user_playlist'] = user_playlist
    
    request.session.save() 
    print("#"*30)
    print(f"save session {request.session['user_data']} and {request.session['user_playlist']}")
    return JsonResponse({"success": True})

    
def get_user_music_list(request):
    PLAYLIST = "我的最愛"
    if request.method != 'POST':
        return HttpResponse('error')
    # 解析 JSON 数据
    data = json.loads(request.body)
    method = data.get('method')
    sql_user_music_list = SQL_music_list(config= user.lib.sql.config.DB_CONFIG_user_music_list, table_name= switch_key(request.session['email']))

    if method == 'insert':
        return JsonResponse(json.dumps({'success': sql_user_music_list.save_data(music_ID_list= json.dumps([data.get('music_ID')],indent=4) , music_list= data.get('playlist' , PLAYLIST),)}), safe=False)
    elif method == 'get':
        return JsonResponse(list(sql_user_music_list.get_music_list(music_list= data.get('playlist' , PLAYLIST))), safe=False)
    elif method == 'delete':
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_data(music_ID_list= json.dumps([data.get('music_ID')] , indent=4) , music_list=  data.get('playlist' , PLAYLIST))}), safe=False)
    elif method == 'favorite':
        return JsonResponse(json.dumps({'success': sql_user_music_list.setfavorite(music_ID_list= json.dumps([data.get('music_ID')] , indent=4))}), safe=False)
    elif method == 'get_playlists':
        return JsonResponse({"success": True, "data": sql_user_music_list.get_playlists()})
    

    sql_user_music_list.close()

def get_user_show_data(request): 
        if request.method != 'POST':
            return HttpResponse('error')
        if request.session['user_data'] is  None:
            save_session(request= request)

        return HttpResponse(json.dumps({
                    "success": True ,
                    "user_data": request.session['user_data'], 
                    "user_playlists": request.session['user_playlist']}))


def hello(request):
    tkey = request.session['email']
    if tkey.startswith('#'):
        key = key[1:]
    else:
        key = tkey.split("@")[0]    
    sql_user_music_list = SQL_music_list(user.lib.sql.config.DB_CONFIG_user_music_list,table_name= key)
    music_ID_list = sql_user_music_list.get_music_list()
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
        email = request.user.email
        name = request.user.first_name
        request.session['isLogin'] = True
       
        if(email==''):
            email = "#" + name
            name = None
    else:
        print("未登入")
        name = None
        email = None
        del request.session['email']
        request.session['isLogin'] = False
    request.session['email'] = email
    request.session['key'] = switch_key(request.session['email'])
     
    # 建立個人專輯
    sql = SQL_music_list(user.lib.sql.config.DB_CONFIG_user_music_list,request.session['key'])
    sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)

    sql.create_tables() #建立資料表 
    sql_user.create_tables() #建立資料表   
    sql_user.save_user_profile(
        id = request.session['key'],
        email = request.session['email'],
        username = name
    )
    
    now = timezone.now()
    sql_user.save_user_profile(
    id = request.session['key'],
    email = request.session['email'],
    username = name
    )
    context = {
        'heading': name ,
        'content': email,
        'now': now
    }
    # store session
    request.session.save() 
    # 存各資
    save_session(request= request)
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
    print(form)
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

def profile2(request):
    if request.method == 'POST':
        form_data = {
            'id': request.session['key'],
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'country': request.POST.get('country'),
            'birthday': request.POST.get('birthday'),
            'gender': request.POST.get('gender'),
        }
        sql = SQL_user(user.lib.sql.config.DB_CONFIG_user)
        sql.create_tables() #建立資料表        
        old_data = sql.get_user_data(request.session['key'])
        sql.save_user_profile(**form_data)
        print("成功修改")
        return redirect('/user/data/')
    sql = SQL_user(user.lib.sql.config.DB_CONFIG_user)
    old_data = sql.get_user_data(uid=request.session['key'])
    
    return render(request, 'edit_profile.html', {'form': old_data})