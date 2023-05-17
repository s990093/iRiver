from django.urls import path, include
from . import views
# 123456
app_name = 'user'
urlpatterns = [
    path('test/', views.user_img, name='test'),
    path('save_session/', views.save_session, name='save_session'),
    path('data/', views.data, name='data'),
    path('register/', views.sign_up, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('isLogin/', views.check_login, name='testuser'),
    path('profile2/', views.profile2, name='profile2'),
    path('get_user_show_data/', views.get_user_show_data,
         name='get_user_show_data'),
    path('get_user_music_list/', views.get_user_music_list,
         name='get_user_music_list'),
]
