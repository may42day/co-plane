from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import User
from .token import token_for_account_activation


def email_activation(request, user: User, user_email: str) -> None:
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


def _return_user_obj_by_uid(uid64: str) -> User:
    """Return user if its exists by decoded uid"""
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user


def _is_account_activated_by_token(user: User, token: str) -> True or False:
    """Checking if user exists with current token"""
    if user is not None and token_for_account_activation.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    return False
