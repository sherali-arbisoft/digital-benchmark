from django.db import models
from django.contrib.auth.models import User


class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class UserData(SoftDeleteMixin, CreateUpdateMixin):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(default=None, blank=True, null=True)
    followers_count = models.IntegerField()  # The number of followers this account currently has
    friends_count = models.IntegerField()  # The number of users this account is following
    favourites_count = models.IntegerField()  # The number of Tweets this user has liked in the account’s lifetime
    listed_count = models.IntegerField()  # The number of public lists that this user is a member of
    screen_name = models.CharField(max_length=255)
    statuses_count = models.IntegerField()  # The number of Tweets (including retweets) issued by the user
    user_id = models.CharField(max_length=255)
    user_name = models.TextField()
    user_location = models.CharField(max_length=255, blank=True, null=True, default=None)

    def str__(self):
        return self.user_name


class AuthToken(models.Model):
    resource_owner_key = models.CharField(max_length=255)
    resource_owner_secret = models.CharField(max_length=255)

    def __str__(self):
        return self.resource_owner_secret


class AccessToken(SoftDeleteMixin, CreateUpdateMixin):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    access_token_secret = models.TextField()

    def __str__(self):
        return self.access_token


class Tweet(SoftDeleteMixin, CreateUpdateMixin):
    user_id = models.IntegerField()  # twitter user id
    favorite_count = models.IntegerField()  # Tweet likes
    retweet_count = models.IntegerField()
    tweet_id = models.IntegerField()  # for getting tweet comments
    text = models.TextField()  # status text
    tweet_created = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract = True


class OtherTweet(Tweet):
    screen_name = models.TextField()

    def __str__(self):
        return self.text


class UserTweet(Tweet):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class UserComment(Tweet):
    status_id = models.IntegerField()  # tweet id which has this comment

    def __str__(self):
        return self.text




