from django.urls import path

from . import views

app_name = 'facebook_benchmark'
urlpatterns = [
    path('login/<str:jwt>', views.LoginView.as_view(), name='login'),
    path('login_successful/<str:jwt>/', views.LoginSuccessfulView.as_view(), name='login_successful'),
    path('home/<str:jwt>/', views.HomeView.as_view(), name='home'),
    path('load_page_data/<int:page_id>/', views.LoadPageDataView.as_view(), name='load_page_data'),
]