from django.contrib import admin
from django.urls import path

from user.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('register', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('api/v1/register', UserAPIView.as_view()),
    #path('api/v1/user/<int:pk>', UserAPIUpdate.as_view()),
    path('api/v1/user/<int:pk>', UserAPIDetailedView.as_view()),
]
