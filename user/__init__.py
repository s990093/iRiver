import user.lib.sql.config
from user.lib.sql.sql_login import SQL as sql_login
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_music_list import SQL as SQL_music_list
from user.lib.sql.sql_user import SQL as SQL_user
import user.lib.sql.config as config
default_app_config = 'user.apps.UserConfig'
# 自製


print("#"*30)
print("init sql user app")

# 建立個人資料table name
sql_login(config=config.DB_CONFIG_user).create_tables()
sql_user = SQL_user(config=config.DB_CONFIG_user)
sql_user.create_tables()

SQL_eq(config=config.DB_CONFIG_user).create_table()

SQL_user_setting(config=config.DB_CONFIG_user).create_table()
