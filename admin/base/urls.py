from django.urls import path
from .views import *


urlpatterns = [
    path('', landing, name='landing'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('service/',service, name='service'),
    path('booking', booking, name='booking'),
    path('subscribe/', subscribe, name='subscribe'),
    path('base_login/', base_login, name='base_login'),
    path('room_list/',room_list,name='room_list_user'),




]
