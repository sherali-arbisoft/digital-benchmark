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
    'facebook_benchmark.apps.FacebookBenchmarkConfig', #register facebook_benchmark app
    'twitter_benchmark', #register twitter_benchmark app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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
facebook_graph_api_version = '3.1'
facebook_default_fields_for_page = 'id,displayed_message_response_time,engagement{count},fan_count,name,overall_star_rating,rating_count,talking_about_count,unread_message_count,unread_notif_count,unseen_message_count,verification_status'
facebook_default_fields_for_feed = 'id,backdated_time,created_time,is_eligible_for_promotion,is_hidden,is_popular,is_published,message,message_tags,promotion_status,scheduled_publish_time,shares,story,story_tags,timeline_visibility,updated_time,comments,likes,reactions,to'
fields = facebook_default_fields_for_post = 'id,backdated_time,created_time,is_eligible_for_promotion,is_hidden,is_popular,is_published,message,message_tags,promotion_status,scheduled_publish_time,shares,story,story_tags,timeline_visibility,updated_time,comments,likes,reactions,to'
facebook_default_metrices_for_page_insights = 'page_impressions,page_engaged_users,page_consumptions,page_negative_feedback,page_fans_online,page_actions_post_reactions_total,page_fans,page_fan_removes,page_views_total,page_video_views,page_posts_impressions'
facebook_default_metrices_for_post_insights = 'post_impressions,post_impressions_unique,post_impressions_fan,post_impressions_fan_unique,post_impressions_organic,post_impressions_organic_unique,post_impressions_viral,post_impressions_viral_unique,post_engaged_users,post_negative_feedback,post_negative_feedback_unique,post_engaged_fan,post_clicks,post_clicks_unique,post_reactions_by_type_total'

# twitter_benchmark setting
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
BASE_AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
PROFILE_DATA_URL = 'https://api.twitter.com/1.1/account/verify_credentials.json'
ACCESS_TOKEN_URL= 'https://api.twitter.com/oauth/access_token'
TWEETS_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
COMMENT_URL = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
CONSUMER_KEY = 'LCE85J76ONueBmKn1SpVAjZ0F'
CONSUMER_SECRET = 'eo992TOAXA6n9KNrKy59Qkb8uKmTMRwE3XevUHeoFm3fXihbEJ'
TWEETS_COUNT = 200

try:
    from .local_settings import *
except ImportError:
    pass