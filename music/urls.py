from django.contrib import admin
from django.urls import path
from login import views as login_views
from iRiver import views as iRiver_views
from music  import views as music_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    path('', iRiver_views.iRiver, name='home'),

    path('iRiver/',iRiver_views.iRiver, name='iRiver'),

    # music
    path('discover/', music_views.discover, name='discover'),
    path('search/', music_views.search, name='search'),
    # fun
    path('query_song/', music_views.query_song, name='query_song'),
    path('download/', music_views.download_song, name='download'),
    # path('music_list/', music_views.music_list, name='music_list'),
    # path('admin/', admin.site.urls),
    
    # # 下載
    # path('download/', music_views.download, name='download'),
    # path('download_songs/', music_views.download_songs, name='download_songs'),
    # path('get-music-list/', music_views.get_music_list, name='get_music_list'),
    # path('download_songs/', music_views.download_songs, name='download_songs'),

    # # test
    # path('test/', music_views.test, name='test'),

    # # iRiver
    path('iRiver/', iRiver_views.iRiver, name='iRiver'),
    path('setting/', iRiver_views.setting, name='setting'),
    path('problem/', iRiver_views.problem, name='problem'),
    path('plan/', iRiver_views.plan, name='plan'),

    # login
    # path('login/', login_views.login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

