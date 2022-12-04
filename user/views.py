from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from .forms import *


class HomePage(TemplateView):
    template_name = 'user/HomePage.html'


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/SignUp.html'
    success_url = reverse_lazy('user:home')
