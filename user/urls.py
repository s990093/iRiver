from django.urls import path, include
from . import views

app_name = 'user'
urlpatterns = [
    path('world/', views.hello, name='hello'),
    path('data/', views.data, name='data'),
    path('register/', views.sign_up, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('isLogin/', views.check_login, name='testuser'),
    path('profile/', views.profile, name='profile'),
    path('get_user_music_list/', views.get_user_music_list,name='get_user_music_list'),
]
