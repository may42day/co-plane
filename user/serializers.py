from threading import Thread

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'phone_number', 'state', 'profile_status', 'photo']

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'An account with email address {email} already exists')
        return email
