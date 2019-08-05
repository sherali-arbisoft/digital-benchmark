from django.conf import settings
from django.utils import timezone
import datetime as dt
dt.datetime.now(tz=timezone.utc)

from .models import InstagramProfile,InstagramMediaInsight,InstagramUserMedia,InstagramMediaComments

class InstagramDataParser:

    def parse_profile_data(self, profile_response,app_user_id):
        profile = InstagramProfile()
        profile.insta_uid = profile_response['user']['id']
        profile.app_user_id = app_user_id
        profile.access_token = profile_response['access_token']
        profile.full_name = profile_response['user']['full_name']
        profile.username = profile_response['user']['username']
        profile.is_business = profile_response['user']['is_business']
        profile.save()
        return profile
    
    #send single media insight entry at a time so that we can save insight id in media table by returning saved insignt back to caller one by one
    def parse_media_insight_data(self, media_insights_response,insta_user):
        insight = InstagramMediaInsight()
        insight.insta_user = insta_user
        insight.likes_count = media_insights_response['likes']['count']
        insight.comments_count = media_insights_response['comments']['count']
        insight.media_tags = media_insights_response['tags']
        insight.media_caption = media_insights_response['caption']['text']
        insight.media_type = media_insights_response['type']
        insight.people_tagged = media_insights_response['users_in_photo']
        insight.filter_used = media_insights_response['filter']
        datetime_python=dt.datetime.fromtimestamp(int(media_insights_response['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
        #print(datetime_python)
        insight.post_created_time = datetime_python
        insight.save()
        return insight

    #send single media at a time with media insight id of media saved in previous step
    def parse_media_data(self, fetch_media_response, insta_user, media_insight):
        media = InstagramUserMedia()
        media.media_id = fetch_media_response['id']
        media.insta_user = insta_user
        media.media_insight = media_insight
        media.media_url = fetch_media_response['link']
        media.save()
        return media

    def parse_media_comments(self, fetch_comments_response, media):
        comment = InstagramMediaComments()
        comment.comment_id = fetch_comments_response['id']
        comment.media = media
        comment.comment_text = fetch_comments_response['text']
        comment.comment_by = fetch_comments_response['from']['username']
        comment.save()
        return comment