from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_successful/', views.LoginSuccessfulView.as_view(), name='login_successful'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('load_page_data/<int:page_id>/', views.LoadPageDataView.as_view(), name='load_page_data'),
]