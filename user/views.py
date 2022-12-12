from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView
from rest_framework.permissions import IsAdminUser

from .forms import *
from rest_framework import viewsets, mixins, generics
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer


class HomePage(TemplateView):
    template_name = 'user/HomePage.html'


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/SignUp.html'
    success_url = reverse_lazy('user:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('user:profile', kwargs={'pk':user.pk}))

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'user/SignIn.html'
    success_url = reverse_lazy('user:home')


class LogoutView(LogoutView):
    next_page = reverse_lazy('user:login-main')


class UserProfile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/Profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        pk = self.kwargs['pk']
        if self.request.user.pk == pk:
            return User.objects.filter(pk=pk)
        raise PermissionDenied()


# API
class RegisterUserAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteUserAPI(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)


class UserUpdateAPI(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class UserProfileAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly)
