import json
import queue
from django.http import JsonResponse
from . import search_audio
import asyncio
import multiprocessing
from queue import Queue

import threading
def carwl_query(query):
    # 使用線程同時執行兩個耗時的操作
    search_youtube_queue = queue.Queue()
    search_summary_queue = queue.Queue()

    search_youtube_thread = threading.Thread(target=search_audio.search_youtube, 
                                             args=(query, ))
    search_summary_thread = threading.Thread(target=search_audio.search_artist_summary,
                                              args=(query, ))

    search_youtube_thread.start()
    search_summary_thread.start()

    search_youtube_thread.join()
    search_summary_thread.join()

    # 獲取結果
    detail_json = json.loads(search_youtube_queue.get())
    summary = search_summary_queue.get()

    # 返回JSON響應
    return JsonResponse({'detail': detail_json, 'summary': summary})
