from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('character', views.character),
    path('game', views.game),
    path('main-game', views.main_game),
    path('player', views.player),
    path('shop', views.shop),
    path('logout', views.logout),
]