from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .email_services import email_activation, _return_user_obj_by_uid, _is_account_activated_by_token
from .forms import *
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer


class HomePage(TemplateView):
    """Display home page"""
    template_name = 'user/HomePage.html'


class RegisterUser(CreateView):
    """Creating a new user with sending email letter for activation"""
    form_class = UserRegisterForm
    template_name = 'user/SignUp.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email_activation(self.request, user, form.cleaned_data.get('email'))
        return redirect(reverse('user:login-main'))


def activate_account(request, uid64: str, token: str):
    """Validates data to complete registration"""
    user = _return_user_obj_by_uid(uid64)
    if _is_account_activated_by_token(user, token):
        login(request, user)
        return redirect(reverse('user:profile', kwargs={'pk': user.pk}))
    return redirect('/')


class LoginUser(LoginView):
    """Authenticate user"""
    form_class = LoginForm
    template_name = 'user/SignIn.html'
    success_url = reverse_lazy('user:home')


class LogoutView(LogoutView):
    """Close user session"""
    next_page = reverse_lazy('user:login-main')


class UserProfile(LoginRequiredMixin, DetailView):
    """Display user's profile for owner"""
    model = User
    template_name = 'user/Profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        pk = self.kwargs['pk']
        current_user = self.request.user
        if current_user.pk == pk or current_user.is_staff:
            return User.objects.filter(pk=pk)
        raise PermissionDenied()


def user_update_profile(request, pk: str):
    """Updates user's profile

    Updates 2 models: User and UserSocialMedia. UserSocialMedia updates an existing instance
    or create a new one if something was added to form.
    """
    if request.user.pk != pk:
        raise PermissionDenied()

    if request.method == 'POST':
        form_user_info = UserProfileEdit(request.POST, instance=request.user)
        social_media_obj = UserSocialMedia.objects.filter(user=request.user).first()
        if social_media_obj:
            form_social_media = UserSocialMediaEdit(request.POST, instance=social_media_obj)
        else:
            form_social_media = UserSocialMediaEdit(request.POST)

        if form_user_info.is_valid() and form_social_media.is_valid():
            form_user_info.save()
            if form_social_media.changed_data and social_media_obj:
                form_social_media.save()
            elif form_social_media.changed_data:
                form = form_social_media.save(commit=False)
                form.user = request.user
                form.save()
            return redirect(reverse('user:profile', kwargs={'pk':pk}))
    else:
        user = User.objects.get(pk=pk)
        form_user_info = UserProfileEdit(instance=user)

        try:
            sm = UserSocialMedia.objects.get(user=user)
            form_social_media = UserSocialMediaEdit(instance=sm)
        except Exception:
            form_social_media = UserSocialMediaEdit()

    return render(request, 'user/ProfileEdit.html', context={
        'form_user_info': form_user_info,
        'form_social_media': form_social_media,
    })


# API
class RegisterUserAPI(generics.CreateAPIView):
    """API for creating a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteUserAPI(generics.DestroyAPIView):
    """API for deleting user"""
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)


class UserUpdateAPI(generics.UpdateAPIView):
    """API for updating user info"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
