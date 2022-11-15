from django.contrib import admin
from .models import CustomUser,UserActivity
# Register your models here.

admin.site.register((CustomUser,UserActivity))