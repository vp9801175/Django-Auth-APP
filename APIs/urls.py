from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('home/', views.welcome_User, name="welcome user"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='login'),
    path('all-users/', views.get_all_user, name="all user"),
    path('create-new-user/', views.register_new_user, name="new user"),

    #Blog APIs

    path('get-all-blogs/', views.getAllBlog, name="get all Blog"),
    path('get-blog/<int:blog_id>/', views.getBlogByID, name="get Blog by id"),
    path('create-new-blog/', views.addBlog, name="new Blog"),
    path('delete-blog/<int:blog_id>/', views.deleteBlog, name="delete Blog"),

    #upload
    path('upload/', views.uploadImage, name="image upload"),
]
