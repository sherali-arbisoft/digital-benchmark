from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255)
    user_name = models.TextField()
    screen_name = models.CharField(max_length=255)
    user_location = models.CharField(max_length=255,blank=True, null=True, default=None)
    description = models.TextField(default=None, blank=True, null=True )
    followers_count = models.IntegerField()  # The number of followers this account currently has
    friends_count = models.IntegerField()  # The number of users this account is following
    listed_count = models.IntegerField()  # The number of public lists that this user is a member of
    favourites_count = models.IntegerField()  # The number of Tweets this user has liked in the account’s lifetime
    statuses_count = models.IntegerField()  # The number of Tweets (including retweets) issued by the user


class AuthToken(models.Model):
    resource_owner_key = models.CharField(max_length=255)
    resource_owner_secret = models.CharField(max_length=255)

    def __str__(self):
        return self.resource_owner_secret


class AccessToken(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    access_token_secret = models.TextField()


class Tweets(models.Model):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.IntegerField()  # twitter user id
    text = models.TextField()  # status text
    favorite_count = models.IntegerField()  # Tweet likes
    retweet_count = models.IntegerField()
    created_at = models.DateTimeField()


class OthersTweets(models.Model):
    screen_name = models.TextField()
    user_id = models.IntegerField()  # twitter user id
    text = models.TextField()  # status text
    favorite_count = models.IntegerField()  # Tweet likes
    retweet_count = models.IntegerField()
    created_at = models.DateTimeField()


