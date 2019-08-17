from .models import UserData, UserTweet, OtherTweet, UserComment


class TwitterDataParser:

    @staticmethod
    def parser_user_data(data):
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

    @staticmethod
    def parser_user_tweet(data):
        user_tweet = []
        for tweet_data in data:
            tweet = UserTweet()
            tweet.text = tweet_data.get('text', '')
            tweet.favorite_count = tweet_data.get('favorite_count')
            tweet.retweet_count = tweet_data.get('retweet_count')
            tweet.user_id = tweet_data.get('user').get('id')
            tweet.tweet_id = tweet_data.get('id')
            user_tweet.append(tweet)
            tweet.save()
        return user_tweet

    @staticmethod
    def parser_other_tweet(data):
        other_tweet_for_view = []
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
            other_tweet_for_view.append(other_tweet)
            other_tweet.save()
        return {'tweets': other_tweet_for_view,
                'screen_name': screen_name
                }

    @staticmethod
    def parser_user_comment(data):
        user_comment_for_view = []
        for comment_data in data:
            user_comment = UserComment()
            user_comment.favorite_count = comment_data.get('favorite_count')
            user_comment.status_id = comment_data.get('in_reply_to_status_id')
            user_comment.text = comment_data.get('text')
            user_comment.tweet_id = comment_data.get('id')
            user_comment.retweet_count = comment_data.get('retweet_count')
            user_comment.user_id = comment_data.get('user').get('id')
            user_comment_for_view.append(user_comment)
            user_comment.save()
        return user_comment








