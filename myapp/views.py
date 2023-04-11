from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
import requests
from myapp.lib import download_audio,search_audio
import json
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import music
from mutagen.mp3 import MP3


def home(request):
    client_ip_address = request.META.get('REMOTE_ADDR')
    print(f"Client IP address: {client_ip_address}")
    # do something else
    return render(request, 'home/index.html')


def play(request):
    music_info = get_music_list(request)
    return render(request, 'play/test.html', context={'music_info': music_info})
def music_list(request):
    music_info = get_music_list(request)
    return render(request, 'music_list/index.html', context={'music_info': music_info})

def get_music_list(request):
    music_folder = os.path.join(settings.MEDIA_ROOT, 'music')
    music_files = os.listdir(music_folder)
    music_list = []
    for file in music_files:
        music_file_path = os.path.join(music_folder, file)
        audio = MP3(music_file_path)
        title = os.path.splitext(file)[0]  # 获取文件名的基本名称（不包括扩展名）
        music_list.append({
            'title': title,
            'artist': audio['TPE1'].text[0] if 'TPE1' in audio else '',
            'duration': str(int(audio.info.length // 60)) + ':' + str(int(audio.info.length % 60)).zfill(2),
            'url': '{}{}'.format('/media/music/', file),
        })
    return JsonResponse({'musicList': music_list})



def crawl(request):
    text = request.GET.get('text', '')
    detail_json = json.loads(search_audio.search_youtube(text))

    # 檢查每個 video 的 img，若為 None，則改成預設圖片路徑
    for video in detail_json['videos']:
        if video['img'] is None:
            video['img'] = '/static/img/music_img.jpg'
        if video['author_img'] is None:
            video['author_img'] = '/static/img/music_author_icon_None.jpg'

    return JsonResponse(detail_json)


def download(request):
    url = request.GET.get('url')
    r = download_audio.action(url)
    if r == "Download complete!":
        return JsonResponse({'success': True, 'message': '{r}'})
    else:
        return JsonResponse({'success': False, 'message': 'Download failed!'})
    
def test(request):
    musics = music.objects.all()
    print(musics)
    return render(request, 'test/test.html', {'musics': musics})

