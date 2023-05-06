import sql
import config
import json

if __name__ == '__main__':
    # Create a SQL object
    sql = sql.SQL(config.DB_CONFIG)
    sql.create_tables()

    r = sql.get_artists(artist='RADWIMPS')

    print(r)

    sql.close()
