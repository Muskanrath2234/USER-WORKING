from django.contrib import admin
from .views import *
from .models import *


admin.site.site_header= "USER"
admin.site.register(Subscription)
