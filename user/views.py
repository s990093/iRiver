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
import user.lib.sql.config as config
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.sql.sql_social import SQL as SQL_social
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from user.lib.switch_key import switch_key
from user.lib.get_data import get_avatar_url,get_line_data,get_google_data,get_line_user_email,get_id_token
from user.lib.print_color import print_color , print_have_line


def save_session(request):
    UID = switch_key(request.session['email'])
    sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
    
    user_data = sql_user.get_user_show_data(uid=UID)
    request.session['user_data'] = user_data

    sql_user_music_list = SQL_music_list(config= user.lib.sql.config.DB_CONFIG_user_music_list, table_name= switch_key(request.session['email']))
    sql_user_music_list.create_tables()
    user_playlist = sql_user_music_list.get_playlists(isAll= True);
    request.session['user_playlist'] = user_playlist

    # eq
    user_eq =  SQL_eq(user.lib.sql.config.DB_CONFIG_user).commit(method= "select" , UID_EQ = UID);
    request.session['user_eq'] = user_eq

    # setting
    user_setting =  SQL_user_setting(user.lib.sql.config.DB_CONFIG_user).commit(method= "select" , UID_SETTING = UID);
    request.session['user_setting'] = user_setting

    # user img 
    # print_have_line(text= user_img(request= request))
    request.session['user_img'] = {"url": str(user_img(request= request))}

    request.session.save() 

    print("#"*30)
    print_color(color= "warning" , text= f"save session {request.session['user_data']} and {request.session['user_playlist']}")
    return JsonResponse({"success": True})

    
def get_user_music_list(request):
    PLAYLIST = "我的最愛"
    if request.method != 'POST':
        return HttpResponse('error')
    # 解析 JSON 数据
    data = json.loads(request.body)
    # print(data)
    method = data.get('method')
    sql_user_music_list = SQL_music_list(config= user.lib.sql.config.DB_CONFIG_user_music_list, table_name= switch_key(request.session['email']))

    if method == 'insert':
        return JsonResponse(json.dumps({'success': sql_user_music_list.save_data(music_ID_list= json.dumps([data.get('music_ID')],indent=4) , music_list= data.get('playlist' , PLAYLIST),)}), safe=False)
    elif method == 'get':
        return JsonResponse(list(sql_user_music_list.get_music_list(music_list= data.get('playlist' , PLAYLIST))), safe=False)
    elif method == 'delete':
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_data(music_ID_list= json.dumps([data.get('music_ID')] , indent=4) , music_list=  data.get('playlist' , PLAYLIST))}), safe=False)
    elif method == 'delete_playlist':
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_playlist(playlist= data.get('playlist' , PLAYLIST) )}), safe=False)
    elif method == 'favorite':
        return JsonResponse(json.dumps({'success': sql_user_music_list.setfavorite(music_ID_list= json.dumps([data.get('music_ID')] , indent=4))}), safe=False)
    elif method == 'get_playlists':
        return JsonResponse({"success": True, "data": sql_user_music_list.get_playlists()})
    elif method == 'change_playlist':
        return JsonResponse({"success": sql_user_music_list.chang_playlist_name(
            old_playlist_name= data.get('old_playlist_name'),
            new_playlist_name= data.get('new_playlist_name'))})
    

    sql_user_music_list.close()

# 舊款
def get_user_show_data(request): 
        if request.method != 'POST':
            return HttpResponse('error')
        if request.session['user_data'] is  None:
            save_session(request= request)
        return HttpResponse(json.dumps({
                    "success": True ,
                    "user_data": request.session['user_data'], 
                    "user_playlists": request.session['user_playlist'] ,
                    "user_img": user_img(request= request)
                    }))
# 新款
def get_user_session(request): 
        if request.method != 'POST':
            return HttpResponse('error')
        if request.session['user_data'] is  None:
            save_session(request= request)
            # 解析 JSON 数据
        data = json.loads(request.body)
        get = data.get('get')
        if get == "user_eq":
            body = {"user_eq": request.session['user_eq']}
        elif get == "user_setting":
            body = {"user_setting": request.session['user_setting']}
        elif get == "user_show_data":
            body = {"user_data": request.session['user_data'], 
                    "user_playlists": request.session['user_playlist'],
                    "user_img": request.session['user_img']}
        elif get == "all":
            body = {"user_data": request.session['user_data'], 
                    "user_playlists": request.session['user_playlist'],
                    "user_img": request.session['user_img'],
                    "user_eq": request.session['user_eq'],
                    "user_setting": request.session['user_setting']}
        else:
            return HttpResponse('error')
        
        print_have_line(text= body)
        return HttpResponse(json.dumps({
            "success": True,
            "data": body
            }))




def user_img(request):
    tkey=  request.session['email']
    if tkey.startswith('#'):
        flag = 1
        key =  request.session['key']
    else:
        flag = 0
        key = tkey
    sql = SQL_social(user.lib.sql.config.DB_CONFIG_social)
    data = sql.get_extra_data(uid=key)#json
    parsed_data = json.loads(data)#字典
    if(flag==0):
        access_token = parsed_data['access_token']
        url = get_avatar_url(access_token)
    else:
        url = parsed_data['picture_url']
        
    return url


def check_login(request):
    if 'isLogin' in request.session:
        return JsonResponse({'isLogin': request.session['isLogin']})
    else:
        return JsonResponse({'isLogin': False})
    


def test123(request):
    tkey=  request.session['email']
    if tkey.startswith('#'):
        flag = 1
        key =  request.session['key']
    else:
        flag = 0
        key = tkey
    sql = SQL_social(user.lib.sql.config.DB_CONFIG_social)
    data = sql.get_extra_data(uid=key)#json
    parsed_data = json.loads(data)#字典
    if(flag==0):
        access_token = parsed_data['access_token']
        data = get_google_data(access_token)
        return JsonResponse(data)
    else:
        access_token = parsed_data['access_token']
        data = get_line_data(access_token)
        return JsonResponse(data)


# 首頁
def data(request):
    if request.user.is_authenticated:
        print("已登入")
        email = request.user.email
        name = request.user.first_name
        name2= request.user.username                  
        request.session['isLogin'] = True
        if(email==''):
            email = "#" + name2
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

    # create setting
    SQL_eq(config= config.DB_CONFIG_user).regsiter(UID_EQ=switch_key(request.session['email']))
    SQL_user_setting(config= config.DB_CONFIG_user).regsiter(UID_SETTING=switch_key(request.session['email']) )

    
    if sql_user.get_user_data(uid= request.session['key']) is None:
        sql_user.save_user_profile(
        id = request.session['key'],
        email = request.session['email'],
        username = name
        )

    # store session
    request.session.save() 
    # 存各資
    save_session(request= request)
    # 重新導向到登入畫面
    return redirect('/music/discover/')  


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
    sql = SQL_user(user.lib.sql.config.DB_CONFIG_user)
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
        sql.save_user_profile(**form_data)
        print("成功修改")
        return redirect('/user/profile2/')
    old_data = sql.get_user_data(uid=request.session['key'])
    return render(request, 'edit_profile.html', {'form': old_data})


def user_eq(request):
    if request.method != 'POST':
        return JsonResponse({"success": False}) 
    
    body = json.loads(request.body)
    kwargs= body.get("kwargs")
    kwargs["uid"] = switch_key(request.session['key'])
    return JsonResponse({"data": (SQL_eq(user.lib.sql.config.DB_CONFIG_user))
                         .commit(method=  body.get("method") , kwargs= kwargs)})



def user_setting(request):
    if request.method != 'POST':
        return JsonResponse({"success": False})  
    
    body = json.loads(request.body)
    method = body.get("method")
    kwargs= body.get("kwargs")
    kwargs["uid"] = switch_key(request.session['key'])
    return JsonResponse({"data": (SQL_user_setting(user.lib.sql.config.DB_CONFIG_user))
                         .commit(method=  method , kwargs= kwargs)})