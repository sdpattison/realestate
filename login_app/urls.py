from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('user', views.login),
    path('logout', views.logout)
]