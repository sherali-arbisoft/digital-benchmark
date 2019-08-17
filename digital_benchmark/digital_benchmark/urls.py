from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

from accounts.views import LoginView,LogoutView,RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('facebook_benchmark/', include('facebook_benchmark.urls')),
    path('instagram_benchmark/', include('instagram_benchmark.urls')),
    path('accounts/', include('accounts.urls')),
    path('', views.HomeView.as_view()),
    path('accounts/login/', LoginView.as_view()),
    path('accounts/register/', RegisterView.as_view()),
    path('accounts/logout/', LogoutView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns