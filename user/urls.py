from django.contrib import admin
from django.urls import path

from user.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
]
