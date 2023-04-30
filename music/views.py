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
import asyncio
# 自製
import music.lib.sql.config
from music.lib.sql.sql import SQL
from music.lib.web_scutter.youtube import query_youtube
from music.lib.web_scutter.iocn import query_artist_iocn_src
from music.lib.web_scutter.summary import query_summary
from music.lib.web_scutter.music_list import query_music_list




# test bool

test =  True


def search(request):
    query = request.GET.get('query', '')
    context = {'query': query}
    return render(request, './serach_reault.html' , context)

def discover(request):
    return render(request, './discover.html' )

# def music_list(request):
#     artist = request.GET.get('artist', '')
#     index = request.GET.get('index', '')

#     return render(request, './music_list.html', context={'artist': artist, 'index': index})

# 資料庫資料
def query_db_song(request):
    query = request.GET.get('query', '')

    # 資料庫
    try:
        mysql  =  SQL(music.lib.sql.config.DB_CONFIG)
        res = mysql.query(query=query)
        if res is None:
            print("the res is empty")
            return 
    except Exception as e:
        print(f'the res is {e}')
        return 
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

    return JsonResponse(music_list , safe=False)

    
# 網路資料
def query_web_song(request):
    query = request.GET.get('query', '')

    # 網路
    if test:
        print('='*50)
        print(f'get  {query} !!')
    try:
        result = json.loads(query_youtube(query=query))
        print('='*50)
        music_list =  result['music_list']
        statistics =  result['statistics']
    except Exception as e:
        print(e)

    return JsonResponse(music_list , safe=False)
