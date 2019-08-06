"""
Django settings for digital_benchmark project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3-1jc^c3n(fw5sctlo*19&vh$-d6h7-45co-4_%totri3h9=^4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'facebook_benchmark', #register facebook_benchmark app
    'debug_toolbar', # register django-debug-toolbar
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # for django-debug-toolbar
]

ROOT_URLCONF = 'digital_benchmark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'digital_benchmark.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# facebook_benchmark settings
FACEBOOK_GRAPH_API_VERSION = '3.1'
FACEBOOK_APP_ID = '349831992602224'
FACEBOOK_APP_SECRET = 'e3bfa0ed905199eecca00e74631280b7'
FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI = 'http://localhost:8000/facebook_benchmark/login_successful'
FACEBOOK_PERMISSIONS = [ 'manage_pages', 'pages_show_list', 'read_insights']
FACEBOOK_RESPONSE_TYPE = 'code'
FACEBOOK_STATE = '{"{st=state123abc,ds=123456789}"}'
FACEBOOK_LOGIN_URL = f"https://www.facebook.com/v{FACEBOOK_GRAPH_API_VERSION}/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI}&scope={','.join(FACEBOOK_PERMISSIONS)}&response_type={FACEBOOK_RESPONSE_TYPE}&state={FACEBOOK_STATE}"
FACEBOOK_USER_ACCESS_TOKEN_URL = f"https://graph.facebook.com/v{FACEBOOK_GRAPH_API_VERSION}/oauth/access_token"
FACEBOOK_DEFAULT_FIELDS_FOR_PROFILE = ['first_name', 'id', 'last_name']
FACEBOOK_DEFAULT_FIELDS_FOR_ACCOUNTS = [ 'access_token', 'id', 'name' ]
FACEBOOK_GRANT_TYPE = 'fb_exchange_token'
FACEBOOK_DEFAULT_FIELDS_FOR_PAGE = ['displayed_message_response_time','engagement','fan_count','id','name','overall_star_rating', 'ratings{created_time,review_text,rating,recommendation_type}', 'rating_count','talking_about_count','unread_message_count','unread_notif_count','unseen_message_count','verification_status']
FACEBOOK_DEFAULT_FIELDS_FOR_FEED = ['backdated_time','comments{id,message,created_time,from{id},reactions{id,type}}','created_time','id','is_eligible_for_promotion','is_expired','is_hidden','is_instagram_eligible','is_popular','is_published','message','promotion_status','reactions{id,type}','scheduled_publish_time','shares','story','timeline_visibility','updated_time']
FACEBOOK_DEFAULT_FIELDS_FOR_POST = ['backdated_time','comments{id,message,created_time,from{id},reactions{id,type}}','created_time','id','is_eligible_for_promotion','is_expired','is_hidden','is_instagram_eligible','is_popular','is_published','message','promotion_status','reactions{id,type}','scheduled_publish_time','shares','story','timeline_visibility','updated_time']
FACEBOOK_DEFAULT_METRICES_FOR_PAGE_INSIGHTS = ['page_consumptions','page_consumptions_unique','page_engaged_users','page_impressions','page_impressions_nonviral','page_impressions_nonviral_unique','page_impressions_organic','page_impressions_organic_unique','page_impressions_paid','page_impressions_paid_unique','page_impressions_unique','page_impressions_viral','page_impressions_viral_unique','page_negative_feedback','page_negative_feedback_unique','page_post_engagements','page_video_views','page_views_total']
FACEBOOK_DEFAULT_DATE_PRESET_FOR_PAGE_INSIGHTS = 'today'
FACEBOOK_DEFAULT_PERIOD_FOR_PAGE_INSIGHTS = 'days_28'
FACEBOOK_DEFAULT_METRICES_FOR_POST_INSIGHTS = ['post_clicks','post_clicks_unique','post_engaged_fan','post_engaged_users','post_impressions','post_impressions_fan','post_impressions_fan_paid','post_impressions_fan_paid_unique','post_impressions_fan_unique','post_impressions_nonviral','post_impressions_nonviral_unique','post_impressions_organic','post_impressions_organic_unique','post_impressions_paid','post_impressions_paid_unique','post_impressions_unique','post_impressions_viral','post_impressions_viral_unique','post_negative_feedback','post_negative_feedback_unique']

# for django-debug-toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

try:
  from .local_settings import *
except ImportError:
  pass