from django.conf import settings
import datetime as dt

from .models import InstagramProfile, InstagramMediaInsight, InstagramUserMedia, InstagramMediaComments
from .data_provider import InstagramDataProvider


class InstagramDataParser:

    def parse_save_profile_data(self, profile_response, app_user_id):
        user = profile_response.get('user')
        profile = InstagramProfile()
        profile.insta_uid = user.get('id')
        profile.app_user_id = app_user_id
        profile.access_token = profile_response.get('access_token')
        profile.full_name = user.get('full_name')
        profile.username = user.get('username')
        profile.is_business = user.get('is_business')
        profile.save()
        return profile

    def parse_profile_update(self, user_profile_data, current_profile):
        current_profile.follows_count = user_profile_data.get(
            'counts').get('follows', 0)
        current_profile.folowed_by_count = user_profile_data.get(
            'counts').get('followed_by', 0)
        current_profile.media_count = user_profile_data.get(
            'counts').get('media', 0)
        try:
            current_profile.save()
            return f"{current_profile.username} follows {current_profile.follows_count} people, followed by {current_profile.folowed_by_count}, has {current_profile.media_count} posts"
        except Exception as e:
            return False
            raise e
    
    def save_profile_data(self, user_profile_data,app_user_id,access_token):
        profile = InstagramProfile()
        profile.insta_uid=user_profile_data.get('id')
        profile.app_user_id = app_user_id
        profile.access_token = access_token
        profile.full_name = user_profile_data.get('full_name')
        profile.username = user_profile_data.get('username')
        profile.is_business = user_profile_data.get('is_business')
        profile.follows_count = user_profile_data.get(
            'counts').get('follows', 0)
        profile.folowed_by_count = user_profile_data.get(
            'counts').get('followed_by', 0)
        profile.media_count = user_profile_data.get(
            'counts').get('media', 0)
        try:
            profile.save()
        except Exception as e:
            raise e

    # send single media insight entry at a time so that we can save insight id in media table by returning saved insignt back to caller one by one
    def parse_media_insight_data(self, all_user_media, insta_user, access_token):
        comments_count = 0
        for media in all_user_media:
            insight = InstagramMediaInsight()
            insight.insta_user = insta_user
            insight.likes_count = media.get('likes').get('count')
            insight.comments_count = media.get('comments').get('count')
            insight.media_tags = media.get('tags')
            insight.media_caption = media.get('caption').get('text')
            insight.media_type = media.get('type')
            insight.people_tagged = media.get('users_in_photo')
            insight.filter_used = media.get('filter')
            datetime_python = dt.datetime.fromtimestamp(
                int(media.get('created_time'))).strftime('%Y-%m-%d %H:%M:%S')
            insight.post_created_time = datetime_python
            insight.save()
            media_just_saved = self.parse_media_data(
                media, insta_user, insight)
            dataProvider1 = InstagramDataProvider(access_token)
            this_media_comments = dataProvider1.get_media_comments(
                media.get('id'))
            comments_count += len(this_media_comments)
            for comment in this_media_comments:
                comments_just_saved = self.parse_media_comments(
                    comment, media_just_saved)
        return [f"{len(all_user_media)} posts fetched and added for Instagram user {insta_user.username}", f"{comments_count} comments saved for user {insta_user.username}"]

    # send single media at a time with media insight id of media saved in previous step
    def parse_media_data(self, fetch_media_response, insta_user, media_insight):
        media = InstagramUserMedia()
        media.media_id = fetch_media_response.get('id')
        media.insta_user = insta_user
        media.media_insight = media_insight
        media.media_url = fetch_media_response.get('link')
        media.save()
        return media

    def parse_media_comments(self, fetch_comments_response, media):
        comment = InstagramMediaComments()
        comment.comment_id = fetch_comments_response.get('id')
        comment.media = media
        comment.comment_text = fetch_comments_response.get('text')
        comment.comment_by = fetch_comments_response.get(
            'from').get('username')
        comment.save()
        return comment
