from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
import requests
from music.lib import download_audio, search_audio
import json
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import music
from collections import Counter
from music.lib.sql.sql import SQL
import music.lib.sql.config
import threading
import re
import asyncio
from music.lib.crawl import carwl_query
from music.lib.clear_str import clear_title


detail_json = {}
most_common_artist = ''
most_common_artist_url = ''
most_common_artist_img_url = ''
artist = ''


def search(request):
    query = request.GET.get('query', '')
    context = {'query': query}
    return render(request, './serach_reault.html' , context)

def discover(request):
    return render(request, './discover.html' )

def music_list(request):
    artist = request.GET.get('artist', '')
    index = request.GET.get('index', '')

    if not artist:
        artist = most_common_artist
    if not index:
        index = 0
    return render(request, './music_list.html', context={'artist': artist, 'index': index})


def get_music_list(request):
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    mysql.create_tables()
    
    r = mysql.get_all_artist_song(artist=artist)
    print('='*30)
    print(f'get music_data {artist}')
    
    # 轉list
    result_list = []
    for row in r:
        result_dict = { 'artist': row[1]
                       , 'title': row[2], 'music_ID': row[3]
                       , 'artist_url': row[4], 'keywords': row[5]
                       , 'views' : row[6], 'publish_time': row[7]}
        result_list.append(result_dict)

    return JsonResponse({'musicList': result_list})


def search_youtube_thread(text):
    result = search_audio.search_youtube(text)
    print(result)

def search_summary_thread(artist):
    result = search_audio.search_artist_summary(artist)
    print(result)

# 爬蟲
def crawl(request):
    global  detail_json, most_common_artist, most_common_artist_url, most_common_artist_img_url,artist
    
    query = request.GET.get('query', '')
    
    print('*'*50)
    print(f'get  {query} !!')
    try:
        detail_json = json.loads(search_audio.search_youtube(query=query))
    except Exception as e:
        print(e)

    # 统计所有艺术家的出现次数
    artists = [video["artist"] for video in detail_json["videos"]]
    counter = Counter(artists)
    most_common_artist = counter.most_common(1)[0][0]
    most_common_artist_url = next((video["artist_url"] for video in detail_json["videos"] if video["artist"] == most_common_artist), None)
    most_common_artist_img_url = next((video["artist_img_url"] for video in detail_json["videos"] if video["artist"] == most_common_artist), None)
    artist = most_common_artist
    # 更改
    show_details_json =  detail_json
    for video in detail_json["videos"]:
        video["title"] = clear_title(title=video['title'] ,artist=most_common_artist) 
    for video in show_details_json["videos"]:
        if video["artist"] != most_common_artist:
            video["artist"] = f"{video['artist']}"
            
    return JsonResponse(show_details_json)

def query_song(request):
    query = request.GET.get('query', '')

    try:
        mysql  =  SQL(music.lib.sql.config.DB_CONFIG)
        res = mysql.query(query=query)
        print(len(res))
        if res is None:
            print("the res is empty")
            return 
    except Exception as e:
        print(f'the res is {e}')
        return 
    
    result_list = []
    for row in res:
        result_dict = {'artist': row[1], 
                        'title': row[2], 
                        'music_ID': row[3],
                        'artist_url': row[4],
                        'keywords': row[5],
                        'views' : row[6],
                        'publish_time' :row[7]}
        result_list.append(result_dict)

    # 改
    # print('*'*30)
    # print(result_list)
    
    return JsonResponse(result_list , safe=False)
    
        
    
def download(request):
    
    selection = request.GET.get('selection' , '')
    song = detail_json["videos"][int(selection) - 1]["title"]

    for res in detail_json["videos"]:
        if res['title'] == song:
            result = res
            break

    song_info_str = download_audio.download(
        result['music_ID'],
        result['url'],
        result['img_url'],
        result['artist_url'],
        result['artist_img_url'],
        result['artist'],
        result['title']
      )

    try:
        song_infos_lsit = []
        if song_info_str is not None:
            song_info = json.loads(song_info_str)
            song_infos_lsit.append(song_info)
            # print(song_infos_lsit[0]['artist'])
            # 寫入資料庫s
            if song_info is not None:
                mysql = SQL(music.lib.sql.config.DB_CONFIG)
                mysql.create_tables()
                mysql.save_data(song_infos=json.dumps(song_infos_lsit))  # 使用转换后的JSON格式
                mysql.close()
        else:
             return JsonResponse({'success': False, 'message': 'ok'})
    except Exception as e:
        print(e)
        pass

    # print('*'*20)
    # print(result)
    return JsonResponse({'success': True, 'message': 'ok'})
    


# 定义一个下载任务函数
def download_task(id, url, img_url, artist_url, artist_img_url, artist , title):
    res = download_audio.download(id, url, img_url, artist_url, artist_img_url, artist , title)
    if res is not None:
        return res
    else: 
        return None
    
def download_songs(request):
    artist_url = request.GET.get('artist_url' , '')
    print('download all songs')
    # 获取搜索结果
    ID_list = search_audio.search_musiclist(artist_url)
    # try:
    # except Exception as e:
    #     print(e)
    #     return JsonResponse({'success': False, 'message': 'ok'})

        
    # 定义线程列表和结果列表
    threads = []
    results = []
    # 创建并启动线程，最高并发数为10
    max_threads = 10
    for i in range(0, len(ID_list), 2):
        id, title = ID_list[i:i+2]
        title = clear_title(title=title , artist=most_common_artist)
        res = download_task(id, 
                            f'https://www.youtube.com/watch?v={id}',
                            f'https://i.ytimg.com/vi/{id}/hqdefault.jpg?',
                            most_common_artist_url,
                            most_common_artist_img_url, 
                            most_common_artist, title)
        if res is not None:
            t = threading.Thread(target=lambda: results.append(json.loads(res)))
            threads.append(t)
            t.start()
            
        # 如果线程数达到最高并发数，等待所有线程结束
        if len(threads) == max_threads:
            for t in threads:
                t.join()
            threads.clear()

    # 等待剩余线程结束
    for t in threads:
        t.join()

    # 输出结果
    print(f'總共有{len(results)}首歌')
      # 删除结果列表中为None的元素
    results = [r for r in results if r is not None]

    # 寫入資料庫
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    mysql.create_tables()
    mysql.save_data(song_infos=json.dumps(results , indent=4))

    r = mysql.get_all_artist_song(artist=most_common_artist)
    r = [' '.join(map(str, i)) + '\n' for i in r]
    print(f'{len(r)}首歌')
    print(''.join(r))
    mysql.close()
    
    return JsonResponse({'success': True, 'message': 'ok'})



def test(request):
  
    # print(musics)
    return render(request, './test.html')

