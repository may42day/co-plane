from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView, UpdateView
from rest_framework.permissions import IsAdminUser
from django.core.mail import EmailMessage

from .forms import *
from rest_framework import generics
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer
from .token import token_for_account_activation


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


def email_activation(request, user, user_email):
    """Generates and send a email letter with token to complete registration"""
    email_subject = 'Account activation'
    context = {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_for_account_activation.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }
    message = render_to_string('user/EmailActivationLetter.html', context=context)
    email = EmailMessage(email_subject, message, to=[user_email])
    if email.send():
        messages.success(request,
                         f'<b>{user}</b>, to confirm your account check your <b>{user_email}</b> and click on \
            received activation link to complete the registration.')
    else:
        messages.error(request,
                       f'Problem sending confirmation email to {user_email}, check if you typed it correctly.')


def activate_account(request, uidb64, token):
    """Validates data to complete registration"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_for_account_activation.check_token(user, token):
        user.is_active = True
        user.save()
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


def user_update_profile(request, pk):
    """Updates user's profile"""
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
        'form_user_info':form_user_info,
        'form_social_media':form_social_media,
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

