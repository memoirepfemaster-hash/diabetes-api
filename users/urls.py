# users/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import login
from . import views

urlpatterns = [
    path('login/', login),
    path('register/', views.register),
]