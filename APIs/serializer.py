from django.contrib.auth.models import User
import datetime 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from APIs.models import Blog, Image

# Serializers

class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
    def validate(self,attrs):
        data = super().validate(attrs)
        self.user.last_login = datetime.datetime.now()
        self.user.save()
        print("User is validating")
        refresh = RefreshToken.for_user(self.user)
        # refresh = self.get_token(self.user)
        print("User validated")
        return {'status':200, 'message':'Success', 'payload':{ "token": str(refresh.access_token)}}
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BlogSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='image.image.url', read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image']:
            representation['image'] = self.context['request'].build_absolute_uri(representation['image'])
        return representation

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image','id')

class BlogSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = Blog
        fields = '__all__'
