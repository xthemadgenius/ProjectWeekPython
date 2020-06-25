from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('character', views.character),
    path('character/<int:id>', views.character_details),
    path('chosen', views.chosen),
    path('create/character', views.chosen_create_character),
    path('create/item', views.chosen_create_item),
    path('create/obstacle', views.chosen_create_obstacle),
    # test code to view Other Pages
    path('game', views.game),
    path('boss', views.boss),
    path('main-game', views.main_game),
    path('player', views.player),
    path('shop', views.shop),
    path('logout', views.logout)
]
