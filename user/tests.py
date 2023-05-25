from django.test import TestCase
from user.lib.sql.sql_music_list import SQL as SQL_music_list
import user.lib.sql.config as config
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from user.lib.sql.sql_user import SQL as SQL_user
# Create your tests here.


def test123(request, data):
    name = data['name']
    email = data['email']
    picture = data['picture']
    userid = data['userid']

    sql = SQL_music_list(
        config.DB_CONFIG_user_music_list, request.session['key'])
    sql_user = SQL_user(config.DB_CONFIG_user)
    sql.create_tables()  # 建立資料表

    # create setting
    SQL_eq(config=config.DB_CONFIG_user).regsiter(
        UID_EQ=request.session['key'])
    SQL_user_setting(config=config.DB_CONFIG_user).regsiter(
        UID_SETTING=request.session['key'])

    if sql_user.get_user_data(uid=request.session['key']) is None:
        sql_user.save_user_profile(
            id=request.session['key'],
            email=request.session['email'],
            username=name
        )
