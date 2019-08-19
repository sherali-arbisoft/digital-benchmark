from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_successful/', views.LoginSuccessfulView.as_view(), name='login_successful'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('load_page_data/<int:page_id>/', views.LoadPageDataView.as_view(), name='load_page_data'),
    path('profile/', views.ProfileList.as_view(), name='profile'),
    path('pages/', views.PageList.as_view(), name='pages'),
    path('pages/<int:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('pages/<int:id>/posts/', views.PostList.as_view(), name='page_posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
]