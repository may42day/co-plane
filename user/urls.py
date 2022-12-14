from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from .views import *
from user.views import *



urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register', RegisterUser.as_view(), name='register'),
    path('activate/<str:uid64>/<str:token>', activate_account, name='activate'),
    path('login', LoginUser.as_view(), name='login-main'),
    path('logout', LogoutView.as_view(), name='logout-main'),
    path('profile/<int:pk>', UserProfile.as_view(), name='profile'),
    path('profile/<int:pk>/edit', user_update_profile, name='profile-edit'),
    path('api/v1/register', RegisterUserAPI.as_view()),
    path('api/v1/user/<int:pk>', UserUpdateAPI.as_view()),
    path('api/v1/user/delete/<int:pk>', DeleteUserAPI.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
