from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
import requests
import json
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import music
from collections import Counter
import threading
import re
from urllib.parse import unquote
from multiprocessing import Process, Queue
import concurrent.futures
# 自製
import music.lib.sql.config
from music.lib.sql.sql import SQL
from music.lib.sql.sql import SQL

from music.lib.clear_str import clear_str

from music.lib.web_scutter.youtube import query_youtube
from music.lib.web_scutter.iocn import query_artist_iocn_src
from music.lib.web_scutter.summary import query_summary
from music.lib.web_scutter.music_list import query_music_list

from music.lib.dow import download


# test bool

test =  True


def discover(request):
    return render(request, './discover.html' )

def search(request):
    query = request.GET.get('query', '')
    context = {'query': query}
    return render(request, './serach_reault.html' , context)


def music_list(request):
    artist = request.GET.get('artist', '')
    index = request.GET.get('index', '')

    return render(request, './music_list.html', context={'artist': artist, 'index': index})

def my_music_list(request):
    album = request.GET.get('album', '')
    return render(request, './my_music_list.html')


def get_music_list(request):
    artist = request.GET.get('artist')
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    mysql.create_tables()
    r = mysql.get_all_artist_song(artist=artist)
    print('#'*30)
    print(r)

    result_list = []
    if  r  ==  "()":
        return JsonResponse({'sucess': False})
    
    for row in r:
        result_dict = { 'artist': row[1]
                    , 'title': row[2], 'music_ID': row[3]
                    , 'artist_url': row[4], 'keywords': row[5]
                    , 'views' : row[6], 'publish_time': row[7]}
        result_list.append(result_dict)

    return JsonResponse({'musicList': result_list})

# 資料庫資料
def query_db_song(request):
    query = request.GET.get('query', '')

    if test:
            print('='*50)
            print(f'get db {query} !!')
    # 資料庫
    try:
        mysql  =  SQL(music.lib.sql.config.DB_CONFIG)
        res = mysql.query(query=query)
        if res is None:
            print("the res is empty")
            return JsonResponse({'isLogin':False})
    except Exception as e:
        print(f'the res is {e}')
        return JsonResponse({'isLogin':False})

    music_list = []
    for row in res:
        result_dict = {'artist': row[1], 
                        'title': row[2], 
                        'music_ID': row[3],
                        'artist_url': row[4],
                        'keywords': row[5],
                        'views' : row[6],
                        'publish_time' :row[7]}
        music_list.append(result_dict)
        
    return JsonResponse({'success': True , 'music_list' : music_list}, safe=False)


    
# 網路資料
def query_web_song(request):
    query = request.GET.get('query', '')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_youtube = executor.submit(query_youtube, query) 
    # 網路
    if test:
        print('='*50)
        print(f'get  {query} !!')
    try:
        youtube_result = json.loads(future_youtube.result())
        music_list =  youtube_result['music_list']
        statistics =  youtube_result['statistics']
    except Exception as e:
        print(e)

    return JsonResponse({'success': True , 'music_list' : music_list}, safe=False)



def download_song(request):
    song_str = request.GET.get('song_info')
    song_info = json.loads(unquote(song_str))
    # 使用 ThreadPoolExecutor 讓下載封面圖片和維基百科摘要的工作可以同時進行
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        src = executor.submit(query_artist_iocn_src, song_info['artist'])  # 取得歌手圖片的來源 URL
        summary = executor.submit(query_summary , song_info['artist'])  # 取得歌手維基百科摘要

    music_ID_list = [song_info['music_ID']]
    # 呼叫 download 函式進行歌曲下載，將歌曲 ID、圖片 URL 和歌手圖片 URL 傳入
    success =  download(music_ID_list= music_ID_list ,
                        img_url= song_info['img_url'],
                        cover_img_url= src.result(),
                        artist_img_url= song_info['artist_img_url'],
                        artsit= song_info['artist'])
    params = [{
            'artist': song_info['artist'],
            'title': song_info['title'],
            'music_ID': song_info['music_ID'],
            'artist_url': song_info['artist_url'],
            # TODO remove this null parameter
            'keywords' :  'null',  # 關鍵字暫時設為 null
            'views': '0',  # 歌曲觀看次數暫時設為 0
            'publish_time': '0',  # 歌曲發佈時間暫時設為 0
        }]
    if success is not None:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        mysql.create_tables()  # 建立資料庫表格
        mysql.save_data(song_infos=json.dumps(params))  # 儲存歌曲資訊
        mysql.save_summary(artist=song_info['artist'] , summary=summary.result())  # 儲存歌手摘要
        mysql.close()  # 關閉資料庫連線
        return JsonResponse({"success": True})
    else: 
        return JsonResponse({"success": False})  # 下載歌曲失敗，回傳 False


def download_songs(request):
    return True
#     song_str = request.GET.get('song_info')
#     song_info = json.loads(unquote(song_str))

#     ID_list = query_music_list(url=song_info['url'])
#     print('~'*30)
#     print(ID_list)
  
#     results = []
#     # dow
#     for i in range(0, len(ID_list), 2):
#         id, title = ID_list[i:i+2]
#         title = clear_str(title=title , artist=song_info['artist'])
#         params = {
#         'output_path': f"media/{song_info['artist']}/music/",
#         'url': song_info['url'],
#         'ID': id,
#         'title': title,
#         'artist_url': song_info['artist_url'],
#         'original_artist': song_info['artist'],
#         'max_retry': 2,
#         }

#         # res = download_audio(params=params)
#         # download_img(url=f'https://i.ytimg.com/vi/{id}/hqdefault.jpg', 
#         #             file_name=f'{id}.jpg' ,
#         #             file_dir= f"media/{song_info['artist']}/img/" )
        
#         # if res is not None:
#         #     results.append(json.loads(res))
#         #     download_img(url=song_info['img_url'] ,file_name='artist.jpg' ,file_dir= f"media/{song_info['artist']}/img/")

           
#     # 输出结果
#     print(f'總共有{len(results)}首歌')
#       # 删除结果列表中为None的元素
#     results = [r for r in results if r is not None]

#     # 寫入資料庫
#     mysql = SQL(music.lib.sql.config.DB_CONFIG)
#     mysql.create_tables()
#     mysql.save_data(song_infos=json.dumps(results , indent=4))
    
#     r = mysql.get_all_artist_song(artist=song_info['artist'])
#     r = [' '.join(map(str, i)) + '\n' for i in r]
#     print(f'{len(r)}首歌')
#     print(''.join(r))
#     mysql.close()
    
#     return JsonResponse({'success': True, 'message': 'ok'})

