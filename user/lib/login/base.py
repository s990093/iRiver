from aiohttp import request
import user.lib.sql.config as config
from user.lib.sql.sql_login import SQL as sql_login
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.print_color import print_have_line



def base(userid, email, name, picture, request):
    sql = sql_login(config.DB_CONFIG_user)
    sql.create_tables()
    uid = sql.insert(userid,email)

    print("%" * 30)
    print(uid)
    print(userid)
    print(email)
    print(name)
    print(picture)

    request.session['email'] = email
    request.session['name'] = name
    request.session['picture'] = picture
    request.session['key'] = uid 

    sql = SQL_music_list(config.DB_CONFIG_user_music_list, request.session['key']).create_tables()
    sql_user = SQL_user(config.DB_CONFIG_user)

    # create setting
    SQL_eq(config=config.DB_CONFIG_user).regsiter(
        UID_EQ=request.session['key'])
    SQL_user_setting(config=config.DB_CONFIG_user).regsiter(
        UID_SETTING=request.session['key'])

    if sql_user.get_user_data(uid=request.session['key']) is None:
        sql_user.save_user_profile(
            id=request.session['key'],
            email=request.session['email'],
            username=request.session['name'],
        )
    
 