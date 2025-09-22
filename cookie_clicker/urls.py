from django.urls import path
from . import views

app_name = 'cookie_clicker' #namespacing daw

urlpatterns = [
    path('', views.cookie_clicker_game, name='game'),
    # We'll add more URLs for actions like clicking and upgrading pra unya
]