default_app_config = 'user.apps.UserConfig'
# 自製
import user.lib.sql.config
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.sql.sql_music_list import SQL as SQL_music_list
import user.lib.sql.config as config
from user.lib.sql.sql_eq import SQL as SQL_eq
from user.lib.sql.sql_user_setting import SQL as SQL_user_setting


print("#"*30)
print("init sql user app")

# 建立個人資料table name
sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
sql_user.create_tables()   

SQL_eq(config= config.DB_CONFIG_user).create_table()

SQL_user_setting(config= config.DB_CONFIG_user).create_table()
