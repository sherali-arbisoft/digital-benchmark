from .models import UserData,UserTweet,OtherTweet,UserComment
import datetime


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

    def parser_user_tweet(self, data):
        for tweet_data in data:
            tweet = UserTweet()
            print(tweet_data.get('text'))
            tweet.text = tweet_data.get('text', '')
            tweet.favorite_count = tweet_data.get('favorite_count')
            tweet.retweet_count = tweet_data.get('retweet_count')
            tweet.user_id = tweet_data.get('user').get('id')
            tweet.tweet_id = tweet_data.get('id')
            tweet.save()

    def parser_other_tweets(self, data):
        screen_name = data['screen_name']
        other_tweets_list = data['tweets']
        for tweet in other_tweets_list:
            other_tweet = OtherTweet()
            other_tweet.screen_name = screen_name
            other_tweet.text = tweet.get('text')
            other_tweet.favorite_count = tweet.get('favorite_count')
            other_tweet.retweet_count = tweet.get('retweet_count')
            other_tweet.user_id = tweet.get('user').get('id')
            other_tweet.tweet_id = tweet.get('id')
            other_tweet.save()

    def parser_user_comment(self, data):
        for comment_data in data:
            user_comment = UserComment()
            user_comment.favorite_count = comment_data.get('favorite_count')
            user_comment.status_id = comment_data.get('in_reply_to_status_id')
            user_comment.text = comment_data.get('text')
            user_comment.tweet_id = comment_data.get('id')
            user_comment.retweet_count = comment_data.get('retweet_count')
            user_comment.user_id = comment_data.get('user').get('id')
            user_comment.save()








