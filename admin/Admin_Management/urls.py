from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('login/', admin_login, name='admin_login'),
     path('register/', register_user, name='register'),
      path('view_all_user/', view_all_users, name='view_all_users'),
    path('view_profile/', view_profile, name='view_profile'),
    path('editprofile/', editprofile, name='editprofile'),
    path('user_logout/', user_logout, name='user_logout'),
     path('verifyEmail', verifyOPT, name='verifyEmail'),
     path('budget/',budget,name='budget')
]
