from django.urls import path, include
from . import views

app_name = 'iRiver'

urlpatterns = [
    path('iRiver/', views.iRiver, name='iRiver'),
    path('setting/', views.setting, name='setting'),
    path('problem/', views.problem, name='problem'),
    path('plan/', views.plan, name='plan'),
    # test
    path('test/', views.test, name='test'),
]
