from aiohttp import request
from django.shortcuts import redirect
import user.lib.sql.config as config
from user.lib.sql.sql_login import SQL as sql_login
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.print_color import print_have_line
# 自製
from user.lib.data.session import save_session


def base(userid, email, name, user_img_url, request):
    sql = sql_login(config.DB_CONFIG_user)
    sql_user = SQL_user(config.DB_CONFIG_user)
    # 檢查第是否有帳號
    if sql.check_if_userid_exists(userid=userid) is None:
        uid = sql.insert(userid, email)

        sql_user.save_user_profile(
            id=uid,
            email=request.session['email'],
            username=request.session['name'],

        )
        sql = SQL_music_list(config.DB_CONFIG_user_music_list,
                             uid).create_tables()
        # create setting
        SQL_eq(config=config.DB_CONFIG_user).regsiter(
            UID_EQ=uid)

        SQL_user_setting(config=config.DB_CONFIG_user).regsiter(
            UID_SETTING=uid)

        # save session
    save_session(request=request,
                 uid=uid,
                 user_img=user_img_url',
                 name=name,
                 email=email,
                 )
