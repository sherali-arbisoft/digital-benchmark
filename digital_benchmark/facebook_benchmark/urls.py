from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_successful/', views.LoginSuccessfulView.as_view(), name='login_successful'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('load_page_data/<int:page_id>/', views.LoadPageDataView.as_view(), name='load_page_data'),
    path('fetch_facebook_profile/<str:user_access_token>/', views.FetchFacebookProfile.as_view(), name='fetch_facebook_profile'),
    path('facebook_profile/', views.FacebookProfileDetail.as_view(), name='facebook_profile_detail'),
    path('pages/', views.PageList.as_view(), name='pages'),
    path('pages/<int:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('posts/', views.PostList.as_view(), name='posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('pages/<int:page_id>/posts/', views.PagePostList.as_view(), name='page_posts'),
    path('posts/<str:post_id>/revisions/', views.PostRevisionsList.as_view(), name='post_revisions'),
    path('posts/<str:post_id>/revisions/latest', views.PostLatestRevision.as_view(), name='post_latest_revision')
]