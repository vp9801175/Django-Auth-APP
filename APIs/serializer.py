from django.contrib.auth.models import User
import datetime , random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

# Serializers

class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
    def validate(self,attrs):
        data = super().validate(attrs)
        # refresh = self.get_token(self.user)
        self.user.last_login = datetime.datetime.now()
        self.user.save()
        refresh = RefreshToken.for_user(self.user)
        return {'status':200, 'message':'Success', 'payload':{ "token": str(refresh.access_token)}}
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']