from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls import static
app_name = 'instagram_benchmark'
 
 
urlpatterns = [
   path('auth', views.AuthView.as_view(), name='auth'),
   path('connection_success', views.ConnectionSuccessView.as_view(), name='connection_success'),
   path('fetch_data/<str:insta_id>/', views.FetchDataView.as_view(), name='fetch_data'),
   path('connect', views.InstaConnectView.as_view(), name='connect'),
   path('crawl', views.InstaCrawlerView.as_view(), name='crawl'),
]