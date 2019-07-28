from django.db import models

class UserData(models.Model):
    user_id = models.CharField(max_length=255)
    user_name = models.TextField()
    screen_name = models.CharField(max_length=255)
    user_location = models.CharField(max_length=255)
    description = models.TextField(default=None, blank=True, null=True )
    followers_count = models.IntegerField()#The number of followers this account currently has
    friends_count = models.IntegerField() #The number of users this account is following
    listed_count = models.IntegerField() #The number of public lists that this user is a member of
    favourites_count = models.IntegerField() #The number of Tweets this user has liked in the account’s lifetime
    statuses_count = models.IntegerField() #The number of Tweets (including retweets) issued by the user
