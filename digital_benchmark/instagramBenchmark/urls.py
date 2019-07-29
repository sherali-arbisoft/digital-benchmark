from django.urls import path

from . import views

app_name = 'instagramBenchmark'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('insta_login', views.insta_login, name='insta_login')
]