from music.lib.sql.sql_class import SQL

import music.lib.sql.config as config

print("#"*30)
print("init sql music app")

sql = SQL(config.DB_CONFIG)
sql.create_table(table_name="songs")
sql.create_table(table_name="hot")
sql.create_table(table_name="style")
sql.create_table(table_name="year")
sql.create_table(table_name="leaderboard")
sql.close()
