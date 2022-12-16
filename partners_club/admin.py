from django.contrib import admin
from .models import *


@admin.register(PartnersClub)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'owner', 'status']
    ordering = ['pk']
    list_per_page = 30

