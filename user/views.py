from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, DetailView
from rest_framework.permissions import IsAdminUser
from django.core.mail import EmailMessage

from .forms import *
from rest_framework import generics
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer
from .token import token_for_account_activation


class HomePage(TemplateView):
    template_name = 'user/HomePage.html'


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/SignUp.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        email_activation(self.request, user, form.cleaned_data.get('email'))
        return redirect(reverse('user:login-main'))


def email_activation(request, user, user_email):
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
