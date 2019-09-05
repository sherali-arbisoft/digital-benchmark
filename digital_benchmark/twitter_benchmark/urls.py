from django.urls import path
from . import  views

app_name = 'twitter_benchmark'

urlpatterns = [
    path('login/',views.LoginView.as_view()),
    path('success/',views.SuccessView.as_view()),
    path('auth/',views.AuthView.as_view(),name ='auth'),
]