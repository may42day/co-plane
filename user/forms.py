from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm

from .models import User, UserSocialMedia


class UserRegisterForm(forms.ModelForm):
    repeat_password = forms.CharField(label='Repeat password',
                                      widget=forms.PasswordInput(attrs={
                                          'placeholder': 'Repeat password',
                                          'class': 'form-control',
                                      }))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email',
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control',
            }),
        }

    def clean_repeat_password(self):
        data = self.cleaned_data
        if data['password'] != data['repeat_password']:
            return 'Passwords do NOT match!'
        return data['repeat_password']

    def clean_email(self):
        email = self.cleaned_data['email']
        email_exists = User.objects.filter(email__iexact=email)
        if email_exists:
            return f'An account with email address {email} already exists'
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control',
                               }))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Password',
                                   'class': 'form-control',
                               }))


class UserProfileEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileEdit, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True
    class Meta:
        model = User
        fields = ['state', 'phone_number', 'profile_status', 'photo', 'email', 'first_name', 'last_name']
        widgets = {
            'state': forms.Select(attrs={
                'placeholder': 'US state ',
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'profile_status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'readonly': 'readonly',

            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name',
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name',
                'class': 'form-control',
            }),
        }


class UserSocialMediaEdit(forms.ModelForm):
    class Meta:
        model = UserSocialMedia
        fields = ['website', 'instagram', 'facebook', 'twitter', 'youtube']
        widgets = {
            'website': forms.TextInput(attrs={
                'placeholder': 'personal website',
                'class': 'form-control',
            }),
            'instagram': forms.TextInput(attrs={
                'placeholder': 'instagram',
                'class': 'form-control',
            }),
            'facebook': forms.TextInput(attrs={
                'placeholder': 'facebook',
                'class': 'form-control',
            }),
            'twitter': forms.TextInput(attrs={
                'placeholder': 'twitter',
                'class': 'form-control',
            }),
            'youtube': forms.TextInput(attrs={
                'placeholder': 'youtube',
                'class': 'form-control',
            }),
        }
