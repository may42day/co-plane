from django import forms
from captcha.fields import CaptchaField
from .models import User


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

    def clean_password(self):
        data = self.cleaned_data
        if data['password'] != data['repeat_password']:
            return 'Passwords do NOT match!'
        return data['repeat_password']

