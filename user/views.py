from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import model_to_dict
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from .forms import *
from rest_framework import generics
from .models import *
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView


class HomePage(TemplateView):
    template_name = 'user/HomePage.html'


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/SignUp.html'
    success_url = reverse_lazy('user:home')


class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIDetailedView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'user/SignIn.html'
    success_url = reverse_lazy('user:home')


class LogoutView(LogoutView):
    next_page = reverse_lazy('user:login')
