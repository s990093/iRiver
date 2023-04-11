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
from django.urls import path
from myapp import views as myapp_views
from login import views as login_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', myapp_views.home, name='home'),
    path('home/', myapp_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('play/', myapp_views.play, name='play'),
    path('music_list/', myapp_views.music_list, name='music_list'),
    path('crawl/', myapp_views.crawl, name='crawl'),
    path('download/', myapp_views.download, name='download'),
    path('get-music-list/', myapp_views.get_music_list, name='get_music_list'),
    # test
    path('test/', myapp_views.test, name='test'),
    # login
    path('login/', login_views.login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# test
#test2
