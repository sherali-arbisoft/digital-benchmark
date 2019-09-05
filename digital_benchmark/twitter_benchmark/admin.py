from django.contrib import admin
from .models import UserData, UserTweet, OtherTweet, UserComment


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = (
                    'user_name', 'screen_name', 'description',
                    'followers_count', 'friends_count', 'listed_count',
                    'favourites_count', 'statuses_count'
                    )
    search_fields = ['user_name', 'screen_name']
    list_filter = ['app_user']
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'


@admin.register(UserTweet)
class UserTweetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'tweet_id', 'text', 'favorite_count', 'retweet_count', 'app_user')
    list_filter = ['app_user']
    search_fields = ['text']
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'


@admin.register(OtherTweet)
class UserTweetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'tweet_id', 'text', 'favorite_count', 'retweet_count', 'screen_name')
    list_filter = ['screen_name']
    search_fields = ['text']
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'


@admin.register(UserComment)
class UserTweetAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'tweet_id', 'text', 'favorite_count', 'retweet_count', 'status_id')
    list_filter = ['status_id']
    search_fields = ['text']
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'


