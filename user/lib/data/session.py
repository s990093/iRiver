import json
from django.http import HttpResponse, HttpResponseRedirect
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.sql.sql_social import SQL as SQL_social
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from django.http import JsonResponse
import user
# 自製
from user.lib.print_color import print_color, print_have_line


def save_session(request, **kwargs):
    print_have_line(text=kwargs)
    UID = kwargs.get('uid')
    request.session['key'] = UID
    sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
    request.session['user_data'] = {'name': kwargs.get('name')}

    request.session['user_img_url'] = {
        'user_img_url': kwargs.get('user_img_url')}

    sql_user_music_list = SQL_music_list(
        config=user.lib.sql.config.DB_CONFIG_user_music_list, table_name=UID)
    sql_user_music_list.create_tables()
    user_playlist = sql_user_music_list.get_playlists(isAll=True)
    request.session['user_playlist'] = user_playlist

    # eq
    user_eq = SQL_eq(user.lib.sql.config.DB_CONFIG_user).commit(
        method="select", UID_EQ=UID)
    request.session['user_eq'] = user_eq

    # setting
    user_setting = SQL_user_setting(user.lib.sql.config.DB_CONFIG_user).commit(
        method="select", UID_SETTING=UID)
    request.session['user_setting'] = user_setting

    request.session.save()

    print("#"*30)
    print_color(color="warning",
                text=f"save session {request.session['user_data']} and {request.session['user_playlist']}")
    return JsonResponse({"success": True})


def get_user_session(request, uid):
    if request.method != 'POST':
        return HttpResponse('error')
    if request.session['user_data'] is None:
        save_session(request=request, uid=uid)
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
                "user_img": request.session['user_img_url']}
    elif get == "all":
        body = {"user_data": request.session['user_data'],
                "user_playlists": request.session['user_playlist'],
                "user_img_url": request.session['user_img_url'],
                "user_eq": request.session['user_eq'],
                "user_setting": request.session['user_setting']}
    else:
        return HttpResponse('error')

    print_have_line(text=body)
    return HttpResponse(json.dumps({
        "success": True,
        "data": body
    }))
