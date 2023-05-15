from django.urls import path ,include
from . import views 

app_name = 'music'
urlpatterns = [
    path('discover/', views.discover, name='discover'),
    path('my_music_list/', views.my_music_list, name='my_music_list'),
    path('search/', views.search, name=' search'),
    # fun
    path('query_db_song/', views.query_db_song, name='query_db_song'),
    path('query_web_song/', views.query_web_song, name='query_web_song'),
    path('download/', views.download_song, name='download'),
    path('download_songs/', views.download_songs, name='download_songs'),
    path('get_music_list/', views.get_music_list, name='get_music_list'),
    path('music_list/', views.music_list, name='music_list'),
    path('test/', views.test, name='test'),
    # # 下載
    # path('download/', views.download, name='download'),
    # path('download_songs/', views.download_songs, name='download_songs'),
    # path('get-music-list/', views.get_music_list, name='get_music_list'),
    # path('download_songs/', views.download_songs, name='download_songs'),
] 

