from django.conf import settings

from .models import InstagramProfile,InstagramMediaInsight,InstagramUserMedia

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
    def parse_media_insight_data(self, media_insights_response,insta_user_id):
        insight = InstagramMediaInsight()
        insight.insta_user_id = insta_user_id
        insight.likes_count = media_insights_response['likes']['count']
        insight.comments_count = media_insights_response['comments']['count']
        insight.media_tags = media_insights_response['tags']
        insight.media_caption = media_insights_response['caption']['text']
        insight.media_type = media_insights_response['type']
        insight.people_tagged = media_insights_response['users_in_photo']
        insight.filter_used = media_insights_response['filter']
        insight.post_created_time = media_insights_response['created_time']
        insight.save()
        return insight

    #send single media at a time with media insight id of media saved in previous step
    def parse_media_data(self, fetch_media_response, insta_user_id, media_insight_id):
        media = InstagramUserMedia()
        media.media_id = fetch_media_response['id']
        media.insta_user_id = insta_user_id
        media.media_insight_id = media_insight_id
        media.media_url = fetch_media_response['link']
        media.save()
        return media