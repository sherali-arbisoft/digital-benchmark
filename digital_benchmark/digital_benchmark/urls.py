from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facebook_benchmark/', include('facebook_benchmark.urls')),
    path('twitter_benchmark/', include('twitter_benchmark.urls')),
    path('instagram_benchmark/', include('instagram_benchmark.urls')),
    path('accounts/', include('accounts.urls')),
    path('', views.HomeView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('silk/', include('silk.urls', namespace='silk')),
    ] + urlpatterns