from .models import UserData,Tweets,OthersTweets


class TwitterDataParser:

    def parser_user_data(self, data):
        user_data = UserData()
        user_data.user_id = data.get('id')
        user_data.user_name = data.get('name')
        user_data.screen_name = data.get('screen_name')
        user_data.user_location = data.get('location', '')
        user_data.description = data.get('description', '')
        user_data.followers_count = data.get('followers_count', 0)
        user_data.friends_count = data.get('friends_count', 0)
        user_data.listed_count = data.get('listed_count', 0)
        user_data.favourites_count = data.get('favourites_count', 0)
        user_data.statuses_count = data.get('statuses_count', 0)
        user_data.save()
        return user_data

    def parser_tweets(self, data):
        tweet = Tweets()
        for tweet_data in data:
            tweet.text = tweet_data.get('text', '')
            tweet.created_at = tweet_data.get('created_at')
            tweet.favorite_count = tweet_data.get('favorite_count')
            tweet.retweet_count = tweet_data.get('retweet_count')
            tweet.user_id = tweet_data['user']['id']
            tweet.save()

    def parser_other_tweets(self, data):
        other_tweet = OthersTweets()
        screen_name = data['screen_name']
        other_tweets_list = data['tweets']
        for tweet in other_tweets_list:
            other_tweet.screen_name = screen_name
            other_tweet.text = tweet.get('text')
            other_tweet.created_at = tweet.get('created_at')
            other_tweet.favorite_count = tweet.get('favorite_count')
            other_tweet.retweet_count = tweet.get('retweet_count')
            other_tweet.user_id = tweet.get('')['user']['id']
            other_tweet.save()





