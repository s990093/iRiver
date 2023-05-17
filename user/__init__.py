default_app_config = 'user.apps.UserConfig'
# 自製
import user.lib.sql.config
from user.lib.sql.sql_user import SQL as SQL_user
from user.lib.sql.sql_music_list import SQL as SQL_music_list


# 建立個人資料table name
sql_user = SQL_user(user.lib.sql.config.DB_CONFIG_user)
sql_user.create_tables() #建立資料表   