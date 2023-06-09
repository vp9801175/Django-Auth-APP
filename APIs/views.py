from django.shortcuts import render
from django.contrib.auth.models import User, Group
import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException , ParseError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import UserSerializer, LoginTokenObtainSerializer, BlogSerializer, ImageSerializer
from APIs.models import Blog, Image


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
        # group = Group.objects.filter(name = data.get('role'))
        # if group.exists() == False:
        #     raise ParseError('Invalid role!')
        # user.save()
        # group = Group.objects.get(name = data.get('role'))
        # group.user_set.add(user)
        user.save()
        user_serializer = UserSerializer(user)
        return Response({'status' : status.HTTP_200_OK , 'message' : 'User Created Successfully' , 'payload' : user_serializer.data})
    except Exception as e:
        raise APIException(str(e))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addBlog(request):
    try:
        user_id = request.data.get('user_assoc')
        user = User.objects.get(id=user_id)
        title = request.data.get('title')
        content = request.data.get('content')
        isDeleted = request.data.get('is_deleted')
        image_id = request.data.get('image')
        image = Image.objects.get(id=image_id)
        blog = Blog(user_assoc=user,title=title, content=content, is_deleted=isDeleted)
        if image:
            blog.image = image

        blog.save()
        serialized = BlogSerializer(blog)
        return Response({'message': 'Blog created successfully.', "payload": serialized.data})
    except Exception as e:
        return Response({'message': 'Error creating blog: ' + str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllBlog(request):
    try:
        querySet = Blog.objects.filter(is_deleted=False)
        blog_serialized = BlogSerializer(querySet, many = True)
        return Response({'status': status.HTTP_200_OK, 'payload': blog_serialized.data })
    except Exception as e:
        return Response({'message': 'Error Getting Blog: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlogByID(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        blog_serialized = BlogSerializer(blog)
        return Response({'status': status.HTTP_200_OK, 'payload': blog_serialized.data })
    except Exception as e:
        return Response({'message': 'Error Getting Blog: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteBlog(request,blog_id):
    try:
        print(request.user)
        blog = Blog.objects.get(id=blog_id,is_deleted=False)
        if request.user.id != blog.user_assoc.id:
            return Response({'status':status.HTTP_401_UNAUTHORIZED,'message':'Success','payload':'You are not allow to delete this Blog!'})
        blog.is_deleted = True
        # blog.delete()
        blog.save()
        return Response({'status':status.HTTP_200_OK,'message':'Success','payload':'Record Deleted Successfully!'})
    except Exception as e:
        raise APIException(str(e))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadImage(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_201_CREATED,'message': 'Image uploaded successfully.', "payload": serializer.data})
    else:
        return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'Error creating blog: ' + str(e)})