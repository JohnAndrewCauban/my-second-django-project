from django.urls import path
from . import views

app_name = 'cookie_clicker'

urlpatterns = [
    path('', views.cookie_clicker_game, name='game'),
    path('click/', views.click_cookie, name='click'),
    path('upgrade/', views.upgrade_gpc, name='upgrade'),
    path('buy_autoclicker/', views.buy_auto_clicker, name='buy_autoclicker'),
    path('auto_generate_gold/', views.auto_generate_gold, name='auto_generate_gold'),
    path('reset/', views.reset_game, name='reset'),
]