from aiohttp import request
import user.lib.sql.config as config
from user.lib.sql.sql_login import SQL as sql_login
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.print_color import print_have_line
# 自製
from user.lib.data.session import save_session


def base(userid, email, name, picture, request):
    sql = sql_login(config.DB_CONFIG_user)
    # 檢查第是否有帳號
    if sql.check_if_userid_exists(userid=userid) is None:
        uid = sql.insert(userid, email)

        sql_user.save_user_profile(
            id=uid,
            email=request.session['email'],
            username=request.session['name'],
        )

    # check
    check = sql.check_if_userid_exists(userid=userid)

    sql = SQL_music_list(config.DB_CONFIG_user_music_list,
                         uid).create_tables()
    sql_user = SQL_user(config.DB_CONFIG_user)

    # create setting
    SQL_eq(config=config.DB_CONFIG_user).regsiter(
        UID_EQ=uid)
    SQL_user_setting(config=config.DB_CONFIG_user).regsiter(
        UID_SETTING=uid)

    if sql_user.get_user_data(uid=uid) is None:
        sql_user.save_user_profile(
            id=uid,
            email=request.session['email'],
            username=request.session['name'],
        )

        # save session
    save_session(request=request,
                 uid=uid,
                 user_img=request.session['picture'],
                 name=request.session['name'],
                 email=request.session['email']
                 )
