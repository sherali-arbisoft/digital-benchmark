from requests_oauthlib import OAuth1Session
from django.conf import settings
from .models import AuthToken


class DataProvider:

    def __init__(self, verifier_token, resource_owner_key):
        self.verifier_token = verifier_token
        obj = AuthToken.objects.get(resource_owner_key=resource_owner_key)
        oauth = OAuth1Session(settings.CONSUMER_KEY,
                              client_secret=settings.CONSUMER_SECRET,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=obj.resource_owner_secret,
                              verifier=self.verifier_token)
        oauth_tokens = oauth.fetch_access_token(settings.ACCESS_TOKEN_URL)

        self.access_token = oauth_tokens['oauth_token']
        self.access_token_secret = oauth_tokens['oauth_token_secret']

    def get_user_profile_data(self):
        oauth = OAuth1Session(settings.CONSUMER_KEY,
                              client_secret=settings.CONSUMER_SECRET,
                              resource_owner_key=self.access_token,
                              resource_owner_secret=self.access_token_secret)
        response = oauth.get(settings.PROFILE_DATA_URL)
        return response.json()

    def get_tweets(self):
        oauth = OAuth1Session(settings.CONSUMER_KEY,
                              client_secret=settings.CONSUMER_SECRET,
                              resource_owner_key=self.access_token,
                              resource_owner_secret=self.access_token_secret)
        response = oauth.get(settings.TWEETS_URL)
        return response.json()
