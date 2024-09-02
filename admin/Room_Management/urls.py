# urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path('room_list/', room_list, name='room_list'),
    path('add/', add_room, name='add_room'),
    path('edit/<int:room_id>/', edit_room, name='edit_room'),
    path('delete/<int:room_id>/', delete_room, name='delete_room'),
    path('search/', search_rooms, name='search_rooms'),


]
