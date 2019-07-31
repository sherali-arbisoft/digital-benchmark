from requests_oauthlib import OAuth1Session
from django.conf import settings


class DataProvider:

    def get_user_profile_data(verifier_token,consumer_key, consumer_secret,resource_owner_key,resource_owner_secret):
        oauth = OAuth1Session(consumer_key,
                              client_secret=consumer_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier_token)
        oauth_tokens = oauth.fetch_access_token(settings.ACCESS_TOKEN_URL)

        access_token = oauth_tokens['oauth_token']
        access_token_secret = oauth_tokens['oauth_token_secret']

        # Make the request
        oauth = OAuth1Session(consumer_key,
                              client_secret=consumer_secret,
                              resource_owner_key=access_token,
                              resource_owner_secret=access_token_secret)
        response = oauth.get("https://api.twitter.com/1.1/account/settings.json")
        return response.text
