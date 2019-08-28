from django.conf import settings

from datetime import datetime

from .models import FacebookProfile, Page, Rating, Post, Comment

class FacebookUserDataParser:
    def __init__(self, user_id, facebook_profile_id=None):
        self.user_id = user_id
        self.facebook_profile_id = facebook_profile_id

    def parse_profile(self, profile_response, user_access_token, expires_at):
        facebook_profile, created = FacebookProfile.objects.get_or_create(user_id=self.user_id, defaults={
            'access_token': user_access_token,
            'expires_at': expires_at,
            'facebook_id': profile_response.get('id'),
            'first_name': profile_response.get('first_name'),
            'last_name': profile_response.get('last_name'),
        })
        facebook_profile.save()
        self.facebook_profile_id = facebook_profile.id
        return facebook_profile

class FacebookPageDataParser:
    def __init__(self, facebook_profile_id, page_id=None):
        self.facebook_profile_id = facebook_profile_id
        self.page_id = page_id
    
    def parse_rating(self, rating_response):
        rating = Rating()
        rating.created_time = rating_response.get('created_time', None)
        rating.rating = rating_response.get('rating', 0)
        rating.recommendation_type = rating_response.get('recommendation_type', 'none').upper()
        rating.review_text = rating_response.get('review_text')
        rating.page_id = self.page_id
        rating.save()

    def parse_page(self, page_response, access_token, expires_at):
        defaults = {
            'access_token': access_token,
            'displayed_message_response_time': page_response.get('displayed_message_response_time'),
            'expires_at': expires_at,
            'fan_count': page_response.get('fan_count', 0),
            'name': page_response.get('name'),
            'num_engagements': page_response.get('engagement', {}).get('count', 0),
            'overall_star_rating': page_response.get('overall_star_rating', 0),
            'page_id': page_response.get('id'),
            'rating_count': page_response.get('rating_count', 0),
            'talking_about_count': page_response.get('talking_about_count', 0),
            'unread_message_count': page_response.get('unread_message_count', 0),
            'unread_notif_count': page_response.get('unread_notif_count', 0),
            'unseen_message_count': page_response.get('unseen_message_count', 0),
            'verification_status': page_response.get('verification_status', 'not_verified'),
        }
        for item in page_response.get('insights', {}).get('data'):
            defaults[item['name']] = item['values'][0]['value']
        page, created = Page.objects.update_or_create(page_id=page_response.get('id'), facebook_profile_id=self.facebook_profile_id, defaults=defaults)
        self.page_id = page.id
        return page

    def parse_comment(self, post_id, comment_response):
        return Comment.objects.create(
            comment_id=comment_response.get('id'),
            created_time=comment_response.get('created_time', None),
            from_id=comment_response.get('from', {}).get('id'),
            message=comment_response.get('message'),
            angry_total=comment_response.get('angry', {}).get('summary', {}).get('total_count', 0),
            haha_total=comment_response.get('haha', {}).get('summary', {}).get('total_count', 0),
            like_total=comment_response.get('like', {}).get('summary', {}).get('total_count', 0),
            love_total=comment_response.get('love', {}).get('summary', {}).get('total_count', 0),
            sad_total=comment_response.get('sad', {}).get('summary', {}).get('total_count', 0),
            wow_total=comment_response.get('wow', {}).get('summary', {}).get('total_count', 0),
            post_id=post_id,
        )

    def parse_post(self, post_response):
        post = Post()
        post.backdated_time = post_response.get('backdated_time', None)
        post.created_time = post_response.get('created_time', None)
        post.is_eligible_for_promotion = post_response.get('is_eligible_for_promotion', False)
        post.is_expired = post_response.get('is_expired', False)
        post.is_hidden = post_response.get('is_hidden', False)
        post.is_instagram_eligible = post_response.get('is_instagram_eligible', False)
        post.is_popular = post_response.get('is_popular', False)
        post.is_published = post_response.get('is_published', False)
        post.message = post_response.get('message', None)
        post.post_id = post_response.get('id')
        post.promotion_status = post_response.get('promotion_status')
        post.scheduled_publish_time = post_response.get('scheduled_publish_time', None)
        post.shares = post_response.get('shares', {}).get('count', 0)
        post.story = post_response.get('story', None)
        post.timeline_visibility = post_response.get('timeline_visibility', 'NORMAL').upper()
        post.updated_time = post_response.get('updated_time', None)
        for item in post_response.get('insights', {}).get('data'):
            setattr(post, item['name'], item['values'][0]['value'])
        post.page_id = self.page_id
        post.save()
        return post