from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.welcome_User, name="welcome user"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('all-users', views.get_all_user, name="all user"),
    path('create-new-user', views.register_new_user, name="new user")
]
