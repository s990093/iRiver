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

# 全局設定
login_test = True
formal_url = "https://iriver.ddns.net"
local_url = "http://127.0.0.1:8000"


def base(userid, email, name, user_img_url, request):
    sql = sql_login(config.DB_CONFIG_user)
    sql_user = SQL_user(config.DB_CONFIG_user)
    # 檢查第是否有帳號
    if sql.check_if_userid_exists(userid=userid) is None:
        uid = sql.insert(userid, email)
        sql_user.save_user_profile(
            id=uid,
            email=email,
            username=name,
        )

        SQL_music_list(config=config.DB_CONFIG_user_music_list,
                       table_name=uid).create_tables()

        SQL_eq(config=config.DB_CONFIG_user).insert(
            UID_EQ=uid)

        SQL_user_setting(config=config.DB_CONFIG_user).insert(
            UID_SETTING=uid)
    else:
        uid = sql.insert(userid=userid, email=email)

    sql.close()

    # save session
    save_session(
        request=request,
        uid=uid,
        user_img_url=user_img_url,
        name=name,
        email=email,
    )
