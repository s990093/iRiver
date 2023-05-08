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
from django.urls import reverse
from django.shortcuts import redirect
# 自製
import music.lib.sql.config
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
    url = 'http://127.0.0.1:8000/user/get_user_music_list/'
    csrftoken = request.COOKIES.get('csrftoken')
    session_id = request.COOKIES.get('sessionid')
    headers = {'Cookie': f'csrftoken={csrftoken}; sessionid={session_id};'}
    data = {'method': 'get'}
    headers['X-CSRFToken'] = csrftoken
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        music_list_infos = mysql.get_music_list_infos(music_ID_list= [item[0] for item in json.loads(response.content)])
        print(music_list_infos)
        music_list_infos_json = json.dumps(music_list_infos)
        return render(request, './my_music_list.html', {'music_list_infos': music_list_infos, 
                                                        'music_list_infos_json': music_list_infos_json})     
   




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

    path = os.path.join("media", song_info['artist'], "songs" ,f"{song_info['music_ID']}.mp3")
   
    if os.path.exists(path=path) :
        return JsonResponse({"success": True})
    
    # 使用 ThreadPoolExecutor 讓下載封面圖片和維基百科摘要的工作可以同時進行
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        src = executor.submit(query_artist_iocn_src, song_info['artist'])  # 取得歌手圖片的來源 URL
        summary = executor.submit(query_summary , song_info['artist'])  # 取得歌手維基百科摘要

    music_ID_list = [song_info['music_ID']]
    # 呼叫 download 函式進行歌曲下載，將歌曲 ID、圖片 URL 和歌手圖片 URL 傳入
    success =  download(music_ID_list= music_ID_list , 
                        artist= song_info['artist'],
                        img_url= song_info['img_url'],
                        cover_img_url= src.result(),
                        artist_img_url= song_info['artist_img_url']
                        )
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
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    artist_url = request.GET.get('artist_url')
    artist = request.GET.get('artist')
    music_list_infos = query_music_list(url=artist_url , artist= artist)
    music_list = []

    for song in music_list_infos:
        music_list.append({
            'artist': artist,
            'title':  song['title'],
            'music_ID':  song['music_ID'],
            'artist_url':  artist_url ,
            # TODO remove this null parameter
            'keywords' :  'null',  # 關鍵字暫時設為 null
            'views': '0',  # 歌曲觀看次數暫時設為 0
            'publish_time': '0',  # 歌曲發佈時間暫時設為 0
        })

    music_ID_list_chunks = [music_list[x:x+15] for x in range(0, len(music_list), 10)]
    for chunk in music_ID_list_chunks:
        success = download( music_ID_list=[song['music_ID'] for song in chunk], 
                            artist=artist , 
                            only_dow_song=True, max_thread= 4
                          )
        if success:
            mysql.save_data(song_infos=json.dumps(chunk, indent=4))


    mysql.close()
    
    return JsonResponse({'success': True})

