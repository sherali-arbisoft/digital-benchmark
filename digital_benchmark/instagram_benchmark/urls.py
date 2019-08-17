from django.urls import path

from . import views

app_name = 'instagram_benchmark'


urlpatterns = [
    path('auth', views.AuthView.as_view(), name='auth'),
    path('connection_success', views.ConnectionSuccessView.as_view(), name='connection_success'),
    path('fetch_data', views.FetchDataView.as_view(), name='fetch_data'),
    path('connect', views.InstaConnectView.as_view(), name='connect'),
]