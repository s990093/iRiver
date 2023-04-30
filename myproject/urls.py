"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from login import views as login_views
from iRiver import views as iRiver_views
from music  import views as music_views
from django.conf.urls.static import static
from django.conf import settings


# rule 放app url 到app再轉要得 function
urlpatterns = [

    path('', iRiver_views.iRiver, name='home'),

    path('iRiver/',iRiver_views.iRiver, name='iRiver'),


    # music
    # path('home/', music_views.home, name='home'),
    path('discover/', music_views.discover, name='discover'),
    path('search/', music_views.search, name='search'),
    # fun
    # path('crawl/', music_views.crawl, name='crawl'),
    path('query_web_song/', music_views.query_web_song, name='query_web_song'),
    path('query_db_song/', music_views.query_db_song, name='query_db_song/'),
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
    path('user/', include('login.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

