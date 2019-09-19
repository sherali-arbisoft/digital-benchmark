from django.urls import path,include
from django.conf import settings
from . import views
from django.conf.urls import static
from rest_framework import routers
 
 
app_name = 'instagram_benchmark'
urlpatterns = [
  path('auth', views.AuthView.as_view(), name='auth'),
  path('connection_success', views.ConnectionSuccessView.as_view(), name='connection_success'),
  path('fetch_data/<str:insta_id>/', views.FetchUserDataView.as_view(), name='fetch_data'),
  path('connect', views.InstaConnectView.as_view(), name='connect'),
  path('crawl', views.InstaCrawlerView.as_view(), name='crawl'),
 
  path('profile',views.InstagramProfileList.as_view(),name='profile_detail'),
  path('media',views.InstagramMediaList.as_view(),name='all_media'),
  path('media/revisions/<int:media_id>',views.InstagramMediaRevisionList.as_view(),name='media_revisions'),
  path('media/revision/<int:pk>',views.MediaRevisionDetail.as_view(),name='revision_by_id'),
  path('media/comments/<int:revision_id>',views.MediaRevisionComments.as_view(),name='comments_by_media_id'),
  path('profile/load',views.InstagramUserDataLoad.as_view(),name='create_profile'),
  path('profile/crawl',views.StartInstagramCrawlerView.as_view(),name='crawl_instagram_profile'),
  path('profile/crawl/status/<str:crawler_id>',views.CrawlerStatusCheck.as_view(),name='check_crawler_status'),
  path('profile/crawl/zip/<str:crawler_id>',views.DownloadCrawledImages.as_view(),name='crawled_profile_zip'),
]
