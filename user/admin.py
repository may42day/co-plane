from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'state', 'profile_status', 'is_active']
    ordering = ['state', 'username']
    list_per_page = 30
    search_fields = ['username']
