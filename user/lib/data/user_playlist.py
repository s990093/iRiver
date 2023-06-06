
import json
from django.http import HttpResponse, JsonResponse
from user.lib.sql.sql_music_list import SQL as SQL_music_list
import user.lib.data.session as session
import user.lib.sql.config as config
import user.lib.print_color as print_color


def get_user_music_list(request, uid: str):
    PLAYLIST = "我的最愛"
    print_color.print_have_line(request.body)
    # 解析 JSON 数据
    data = json.loads(request.body)
    # print(data)
    print_color.print_have_line(data)

    method = data.get('method')
    sql_user_music_list = SQL_music_list(
        config=config.DB_CONFIG_user_music_list, table_name=uid)

    if method == 'insert':
        return JsonResponse(json.dumps({'success': sql_user_music_list.save_data(music_ID_list=json.dumps([data.get('music_ID')], indent=4), music_list=data.get('playlist', PLAYLIST),)}), safe=False)
    elif method == 'get':
        return JsonResponse(list(sql_user_music_list.get_music_list(music_list=data.get('playlist', PLAYLIST))), safe=False)
    elif method == 'delete':
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_data(music_ID_list=json.dumps([data.get('music_ID')], indent=4), music_list=data.get('playlist', PLAYLIST))}), safe=False)
    elif method == 'delete_playlist':
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_playlist(playlist=data.get('playlist', PLAYLIST))}), safe=False)
    elif method == 'favorite':
        return JsonResponse(json.dumps({'success': sql_user_music_list.setfavorite(music_ID_list=json.dumps([data.get('music_ID')], indent=4))}), safe=False)
    elif method == 'get_playlists':
        return JsonResponse({"success": True, "data": sql_user_music_list.get_playlists()})
    elif method == 'change_playlist':
        return JsonResponse({"success": sql_user_music_list.chang_playlist_name(
            old_playlist_name=data.get('old_playlist_name'),
            new_playlist_name=data.get('new_playlist_name'))})

    sql_user_music_list.close()
