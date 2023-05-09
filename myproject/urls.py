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
from user import views as login_views
from iRiver import views as iRiver_views
from user import views as user
from music  import views as music_views
from django.conf.urls.static import static
from django.conf import settings

# rule 放app url 到app再轉要得 function
urlpatterns = [
    path('', iRiver_views.iRiver, name='home'),
    path('iRiver/', include('iRiver.urls',namespace='iRiver')),
    path('music/', include('music.urls',namespace='music')),
    path('user/', include('user.urls',namespace='user')),
    path('auth/', include('social_django.urls', namespace='auth')),
    path('auth/complete/google-oauth2/user/data/', user.data),
    path('admin/', admin.site.urls),        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

