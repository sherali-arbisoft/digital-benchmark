from django.urls import path
from . import views

app_name = 'twitter_benchmark'

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('success/', views.SuccessView.as_view()),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('othertweet/<screenname>', views.OtherTweetList.as_view(), name='other_tweet'),
    path('usertweet/', views.UserTweetList.as_view(), name='user_tweet'),
    path('userdata/', views.UserDataList.as_view(), name='user_tweet'),
    path('usertweetbyid/<int:id>/', views.UserTweetByIdList.as_view(), name='tweet_by_id'),
    path('userlatesttweet/<int:id>/', views.UserLatestTweet.as_view(), name='latest_tweet'),
    path('othertweetbyid/<int:id>/', views.OtherTweetByIdList.as_view(), name='other_tweet_by_id'),
    path('otherlatesttweet/<int:id>/', views.OtherLatestTweet.as_view(), name='other_latest_tweet'),
]