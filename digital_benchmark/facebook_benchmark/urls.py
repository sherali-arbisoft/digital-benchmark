from django.urls import path

from . import views

urlpatterns = [
    path('feed/<str:access_token>/', views.feed, name='feed'),
]