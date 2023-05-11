from django.shortcuts import render
from django.contrib.auth.models import User, Group
import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException , ParseError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import UserSerializer, LoginTokenObtainSerializer


# Views.

class LoginView(TokenObtainPairView):
    serializer_class = LoginTokenObtainSerializer
    
@api_view(['GET'])
def welcome_User(request):
    return Response("Welcome to the Django Project")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user(request):
    querySet = User.objects.all()
    user_serialized = UserSerializer(querySet, many = True)
    return Response({'status': status.HTTP_200_OK, 'payload': user_serialized.data })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_new_user(request):
    try:
        data = request.data
        username = data.get('username')
        if User.objects.filter(username = username).exists():
            raise ParseError('Account with this email already exists')
        user = User(username = username, email = data.get('email'), first_name = data.get('first_name'), date_joined = datetime.datetime.now())
        password = data.get('password')
        if password != data.get("confirmPassword"):
            raise ParseError('Password does not match with confirm password')
        user.set_password(password)
        group = Group.objects.filter(name = data.get('role'))
        if group.exists() == False:
            raise ParseError('Invalid role!')
        user.save()
        group = Group.objects.get(name = data.get('role'))
        group.user_set.add(user)
        user.save()
        user_serializer = UserSerializer(user)
        return Response({'status' : status.HTTP_200_OK , 'message' : 'User Created Successfully' , 'payload' : user_serializer.data})
    except Exception as e:
        raise APIException(str(e))