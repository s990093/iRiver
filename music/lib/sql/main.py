import sql
import config
import json

if __name__ == '__main__':
    # Create a SQL object
    sql = sql.SQL(config.DB_CONFIG)
    sql.create_tables()


    r = sql.get_artists(artist='RADWIMPS')
    print(type(r[0]))
    # print (r[0][2])
    result_list = []
    for row in r:
        result_dict = {'id': row[0], 'artist': row[1], 'title': row[2], 'video_id': row[3], 'channel_url': row[4], 'tags': row[5]}
        result_list.append(result_dict)

    print(result_list[0])

    # r = [' '.join(map(str, i)) + '\n' for i in r]
    # print(r[0])
   

    # data = sql.get_all_song(field='music_ID')
    # r = sql.get_all_song(field='music_ID')
    # r = [' '.join(map(str, i)) + '\n' for i in r]
    # print(''.join(r))

    sql.close()
