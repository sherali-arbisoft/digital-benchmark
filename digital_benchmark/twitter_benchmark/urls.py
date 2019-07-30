from django.urls import path
from . import  views

urlpatterns = [
    path('',views.login,name = 'login'),
    path('<int:user_id>/user/',views.user,name = 'user'),
    path('success/',views.success,name = 'success')
]