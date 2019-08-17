from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# urlpatterns = format_suffix_patterns([
#     path('signup/', views.Signup.as_view(), name='signup'),
#     path('login/', views.Login.as_view(), name='login'),
#     path('home/', views.Home.as_view(), name='home')
# ])

app_name = 'accounts'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('home/<str:jwt>/', views.HomeView.as_view(), name='home'),
]