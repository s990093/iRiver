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
import  music.lib.download.img as img
from music.lib.web_scutter.music_ID_info import get_music_ID_info

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
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    music_list_infos = mysql.get_all_artist_song(artist= artist)
    music_list_infos_json = json.dumps(music_list_infos)
    summary_str = (mysql.get_artist_summary(artist= artist))
    summary = ""
    for item in summary_str:
        summary += item[0]
        
    return render(request, './music_list.html', context={'artist': artist, 'index': index , 
                                                         'music_list_infos': music_list_infos,
                                                         'music_list_infos_json': music_list_infos_json,
                                                         'summary': summary
                                                         })

def my_music_list(request):
    music_list = request.GET.get('music_list' , 1)
    url = 'http://127.0.0.1:8000/user/get_user_music_list/'
    csrftoken = request.COOKIES.get('csrftoken')
    session_id = request.COOKIES.get('sessionid')
    headers = {'Cookie': f'csrftoken={csrftoken}; sessionid={session_id};'}
    data = {'method': 'get'}
    headers['X-CSRFToken'] = csrftoken
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.content)

    if response.status_code == 200:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        music_list_infos = mysql.get_music_list_infos(music_ID_list= [item[0] for item in json.loads(response.content)])
        # print(music_list_infos)
        music_list_infos_json = json.dumps(music_list_infos)
        return render(request, './my_music_list.html', {'music_list_infos': music_list_infos, 
                                                        'music_list_infos_json': music_list_infos_json,
                                                        'music_list': music_list
                                                        })     
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
    
    music_ID_list = [song_info['music_ID']]
    # 使用 ThreadPoolExecutor 讓下載封面圖片和維基百科摘要的工作可以同時進行
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # 下載artist 小圖
        executor.submit(img.download_img(url= song_info['artist_img_url'], file_name='artist.jpg',
                                        file_dir=f"media/{song_info['artist']}/img/"))

        # 下載 封面
        executor.submit(img.download_img_base64(url= executor.submit(query_artist_iocn_src, song_info['artist']).result() ,
                                file_name='cover.jpg', file_dir=f"media/{song_info['artist']}/img/"))
        # music_ID info 
        music_ID_info = executor.submit(get_music_ID_info , song_info['music_ID']).result()
    
        #dow summary
        summary = executor.submit(query_summary , song_info['artist'])  # 取得歌手維基百科摘要

        #dow song
        success =  download(music_ID_list= music_ID_list , 
                        artist= song_info['artist'],
                        only_dow_song= True)

    params = [{
            'artist': song_info['artist'],
            'title': song_info['title'],
            'music_ID': song_info['music_ID'],
            'album': 'null',
            'label': 'null',
            'artist_url': song_info['artist_url'],
            'sources': 'pytube',
            'download_status': success,
            'style': 'null',
            'country': 'null',
            'language': 'null',
            'description': music_ID_info['description'],
            'keywords':  music_ID_info['keywords'],  
            'ch_lyrics': music_ID_info['ch_lyrics'],
            'en_lyrics': music_ID_info['en_lyrics'],
            'views': music_ID_info['views'],
            'release_year': '0',
            'publish_time': music_ID_info['publish_time'],  
        }] 
    
    if success is not None:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        mysql.create_tables()  # 建立資料庫表格
        mysql.save_data(song_infos=json.dumps(params) , summary=summary.result())  # 儲存歌曲資訊
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
        music_ID_info = get_music_ID_info(music_ID= song['music_ID'])
        music_list.append({
            'artist': artist,
            'title':song['title'],
            'music_ID': song['music_ID'],
            'album': 'null',
            'label': 'null',
            'artist_url': artist_url,
            'sources': 'pytube',
            'download_status': True,
            'style': 'null',
            'country': 'null',
            'language': 'null',
            'description': music_ID_info['description'],
            'keywords':  music_ID_info['keywords'],  
            'ch_lyrics': music_ID_info['ch_lyrics'],
            'en_lyrics': music_ID_info['en_lyrics'],
            'views': music_ID_info['views'],
            'release_year': '0',
            'publish_time': music_ID_info['publish_time'],  
        })

    music_ID_list_chunks = [music_list[x:x+8] for x in range(0, len(music_list), 10)]
    for chunk in music_ID_list_chunks:
        success = download( music_ID_list=[song['music_ID'] for song in chunk], 
                            artist=artist , 
                            only_dow_song=True, max_thread= 3
                          )
        if success:
            mysql.save_data(song_infos=json.dumps(chunk, indent=4))


    mysql.close()
    
    return JsonResponse({'success': True})

# function

def is_song_exist(request):
    music_ID = request.get('music_ID' , None)
    if music_ID:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        # mysql.query_song()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
        