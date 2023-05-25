from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
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
from user.lib.data.get_data import get_avatar_url, get_line_data, get_google_data, get_line_user_email, get_id_token
from user.lib.print_color import print_color, print_have_line
from user.lib.login.line import line_url, line_callback
from user.lib.login.google import google_url, google_callback
# data
import user.lib.data.session as session
import user.lib.data.user_playlist as user_playlist
import user.lib.data.get_data as get_data

# test
import user.tests as tests

# 舊款


def save_session(request):
    session.save_session(request=request, uid=request.session['key'])


def get_user_music_list(request):
    user_playlist.get_user_music_list(
        request=request, uid=request.session['key'])


# 舊款


def get_user_show_data(request):
    get_data.get_user_show_data(
        request=request, uid=request.session['key'])

# 新款


def get_user_session(request):
    session.get_user_session(
        request=request, uid=request.session['key'])


def check_login(request):
    if 'isLogin' in request.session:
        return JsonResponse({'isLogin': request.session['isLogin']})
    else:
        return JsonResponse({'isLogin': False})

# google 登入


def googleurl(request):
    url = google_url(request)
    return HttpResponseRedirect(url)


def googlecallback(request):
    success = google_callback(request)
    # request.session['isLogin'] = success
    if success:
        print_have_line(text="登入成功")
        print(request.session['name'])
        print(request.session['key'])
        return redirect('/music/discover/')
    else:
        print_have_line(text="登入失敗")
        return redirect('/user/login/')
    # check(request=request,success=success)

# line 登入


def lineurl(request):
    url = line_url(request)
    return HttpResponseRedirect(url)


def linecallback(request):
    success = line_callback(request)
    # request.session['isLogin'] = success
    if success:
        print_have_line(text="登入成功")
        return redirect('/music/discover/')
    else:
        print_have_line(text="登入失敗")
        return redirect('/user/login/')
    # check(request=request,success=success)


def test123(request, data):
    tests.test123(request=request, data=data)

# 註冊


def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print("註冊成功")
            return redirect('/user/login/')  # 重新導向到登入畫面
        else:
            print("註冊錯誤")
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


# 登入
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
            return redirect('/user/data/')  # 重新導向到首頁
        else:
            print("登入錯誤")
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)

# 登出


def log_out(request):
    logout(request)
    request.session['isLogin'] = False
    request.session.save()
    print(request.session.get('isLogin'))
    print("已登出")
    return redirect('/user/login')

# 個人資料


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
    kwargs = body.get("kwargs")
    print_have_line(text=kwargs)
    kwargs['UID_EQ'] = switch_key(request.session['email'])
    return JsonResponse({"data": (SQL_eq(user.lib.sql.config.DB_CONFIG_user))
                         .commit(method=body.get("method"), kwargs=kwargs)})


def user_setting(request):
    if request.method != 'POST':
        return JsonResponse({"success": False})

    body = json.loads(request.body)
    method = body.get("method")
    kwargs = body.get("kwargs")
    kwargs['UID_SETTING'] = switch_key(request.session['email'])

    return JsonResponse({"data": (SQL_user_setting(user.lib.sql.config.DB_CONFIG_user))
                         .commit(method=method, kwargs=kwargs)})
