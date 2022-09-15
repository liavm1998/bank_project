from rest_framework import serializers
from .models import User
from user import jwt
from datetime import datetime, timedelta
from django.conf import settings

"""
my user serializer 
"""
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=126,min_length=6, write_only=True)
    class Meta():
        model = User
        fields=(
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'token'
        )
        read_only_fields = ['token']

    def create(self, validated_data):
        return User.objects.create_User(**validated_data)

    @property
    def token(self):
        token=jwt.encode({
                'username': self.username,
                'email':self.email,
                'exp':datetime.utcnow()+timedelta(hours=12),
            },settings.SECRET_KEY,
            algorithm='HS256')
        return token
    

"""
    the next serailizer are unnecessary and exist in propose of comfort only
"""
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=126,min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['username','password','token']
        read_only_fields = ['token']


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=126,min_length=6, write_only=True)
    class Meta():
        model = User
        fields=(
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'user_balance'
        )