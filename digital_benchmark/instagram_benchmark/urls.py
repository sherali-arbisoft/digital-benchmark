from django.urls import path

from . import views

app_name = 'instagram_benchmark'


urlpatterns = [
    path('', views.index, name='index'),#temporary end point
    path('auth', views.AuthView.as_view(), name='auth'),
    path('login_success', views.LoginSuccessView.as_view(), name='login_success'),
    path('fetch_data', views.FetchDataView.as_view(), name='fetch_data'),
    path('login', views.login, name='login'),
]