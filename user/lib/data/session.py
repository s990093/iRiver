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
    UID = kwargs.get('uid')
    sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
    request.session['user_data'] = {'name': kwargs.get('name'),
                                    'user_img_url': kwargs.get('user_img')}

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
