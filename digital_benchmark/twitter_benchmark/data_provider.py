from requests_oauthlib import OAuth1Session
from django.conf import settings
from .models import AuthToken


class DataProvider:

    def __init__(self, verifier_token, resource_owner_key):
        self.verifier_token = verifier_token
        db_resource_owner_secret = AuthToken.objects.get(resource_owner_key=resource_owner_key)
        oauth = OAuth1Session(settings.CONSUMER_KEY,
                              client_secret=settings.CONSUMER_SECRET,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=db_resource_owner_secret.resource_owner_secret,
                              verifier=self.verifier_token)
        delete_used_auth = AuthToken.objects.filter(resource_owner_key=resource_owner_key)
        delete_used_auth.delete()
        oauth_tokens = oauth.fetch_access_token(settings.ACCESS_TOKEN_URL)
        self.access_token = oauth_tokens['oauth_token']
        self.access_token_secret = oauth_tokens['oauth_token_secret']
        self.oauth = OAuth1Session(settings.CONSUMER_KEY,
                                  client_secret=settings.CONSUMER_SECRET,
                                  resource_owner_key=self.access_token,
                                  resource_owner_secret=self.access_token_secret)

    def get_user_profile_data(self):
        response = self.oauth.get(settings.PROFILE_DATA_URL)
        return response.json()

    def get_user_tweet(self):
        tweets = []
        total_tweets = self.get_user_profile_data().get('statuses_count')
        first_params = {"trim_user": True,
                        "count":  settings.TWEETS_COUNT
                       }
        first_response = self.oauth.get(settings.TWEETS_URL, params=first_params)
        tweets.append(first_response.json())
        if total_tweets > 200:
            lowest_tweet_id = self.get_min_id(first_response.json())
            n = total_tweets
            while n > 0:
                params = {"trim_user": True,
                          "count": settings.TWEETS_COUNT,
                          "max_id": lowest_tweet_id,
                          "exclude_replies": True
                          }
                response = self.oauth.get(settings.TWEETS_URL, params=params)
                next_tweets = response.json()
                n = n-5
                lowest_tweet_id = self.get_min_id(next_tweets)
                tweets.append(next_tweets[1:])
        return tweets[0]

    def get_other_tweet(self, screen_name):
        tweets = []
        total_tweets = self.get_other_tweet_count(screen_name)
        first_params = {"trim_user": True,
                        "count":  settings.TWEETS_COUNT,
                        "screen_name": screen_name
                       }
        first_response = self.oauth.get(settings.TWEETS_URL, params=first_params)
        tweets.append(first_response.json())
        if total_tweets > 200:
            lowest_tweet_id = self.get_min_id(first_response.json())
            n = total_tweets
            while n > 0:
                params = {"trim_user": True,
                          "count": settings.TWEETS_COUNT,
                          "max_id": lowest_tweet_id,
                          "screen_name": screen_name
                          }
                response = self.oauth.get(settings.TWEETS_URL, params=params)
                next_tweets = response.json()
                n = n-5
                lowest_tweet_id = self.get_min_id(next_tweets)
                tweets.append(next_tweets[1:])
        others_tweets = {'tweets': tweets[0],
                         'screen_name': screen_name
                        }
        return others_tweets

    def get_other_tweet_count(self, screen_name):
        first_params = {"trim_user": False,
                        "count": 1,
                        "screen_name": screen_name
                        }
        response = self.oauth.get(settings.TWEETS_URL, params=first_params)
        return response.json()[0]['user']['statuses_count']

    def get_user_comment(self):
        tweets = []
        first_params = {"trim_user": True,
                        "count": settings.TWEETS_COUNT
                        }
        first_response = self.oauth.get(settings.COMMENT_URL, params=first_params)
        tweets.append(first_response.json())
        if len(first_response.json()) > 200:
            lowest_tweet_id = self.get_min_id(first_response.json())
            is_has_comment = True
            while is_has_comment :
                params = {"trim_user": True,
                          "count": settings.TWEETS_COUNT,
                          "max_id": lowest_tweet_id,
                          }
                response = self.oauth.get(settings.COMMENT_URL, params=params)
                next_tweets = response.json()
                lowest_tweet_id = self.get_min_id(next_tweets)
                tweets.append(next_tweets[1:])
                if len(next_tweets) < 200:
                    is_has_comment = False
        return tweets[0]

    def get_min_id(self, data):
        last_tweet = data[-1]
        return last_tweet.get('id')
