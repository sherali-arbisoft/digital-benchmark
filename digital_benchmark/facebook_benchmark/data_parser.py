from django.conf import settings

from datetime import datetime

from .models import FacebookProfile, Page, Rating, Post, Comment

class FacebookUserDataParser:
    def __init__(self, user_id, facebook_profile_id=None, *args, **kwargs):
        self.user_id = user_id
        self.facebook_profile_id = facebook_profile_id

    def parse_profile(self, profile_response, user_access_token, expires_at, *args, **kwargs):
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

    def parse_pages(self, pages_response, *args, **kwargs):
        pages = []
        for page_response in pages_response:
            page, created = Page.objects.get_or_create(page_id=page_response.get('id'), facebook_profile__user_id=self.user_id, defaults={
                'facebook_profile_id': self.facebook_profile_id
            })
            page.access_token = page_response.get('access_token')
            page.name = page_response.get('name')
            pages.append(page)
        return pages

class FacebookPageDataParser:
    def __init__(self, facebook_profile_id, page_id, *args, **kwargs):
        self.facebook_profile_id = facebook_profile_id
        self.page_id = page_id
    
    def _parse_ratings(self, ratings_response, *args, **kwargs):
        for rating_response in ratings_response['data']:
            rating = Rating()
            rating.created_time = rating_response.get('created_time', None)
            rating.rating = rating_response.get('rating', 0)
            rating.recommendation_type = rating_response.get('recommendation_type', 'none').upper()
            rating.review_text = rating_response.get('review_text')
            rating.page_id = self.page_id
            rating.save()

    def parse_page_details(self, page_details_response, *args, **kwargs):
        page, created = Page.objects.get_or_create(id=self.page_id, defaults={
            'facebook_profile_id': self.facebook_profile_id
        })
        page.displayed_message_response_time = page_details_response.get('displayed_message_response_time')
        page.num_engagements = page_details_response.get('engagement', {}).get('count', 0)
        page.fan_count = page_details_response.get('fan_count', 0)
        page.name = page_details_response.get('name')
        page.overall_star_rating = page_details_response.get('overall_star_rating', 0.0)
        page.page_id = page_details_response.get('id')
        page.rating_count = page_details_response.get('rating_count', 0)
        page.talking_about_count = page_details_response.get('talking_about_count', 0)
        page.unread_message_count = page_details_response.get('unread_message_count', 0)
        page.unread_notif_count = page_details_response.get('unread_notif_count', 0)
        page.unseen_message_count = page_details_response.get('unseen_message_count', 0)
        page.verification_status = page_details_response.get('verification_status', 'not_verified')
        page.save()
        if 'ratings' in page_details_response:
            self._parse_ratings(ratings_response=page_details_response.get('ratings'))
        return page
    
    def parse_page_insights(self, page_insights_response, *args, **kwargs):
        page, created = Page.objects.get_or_create(id=self.page_id, defaults={
            'facebook_profile_id': self.facebook_profile_id
        })
        for item in page_insights_response['data']:
            setattr(page, item['name'], item['values'][0]['value'])
        page.save()
        return page

    def parse_comment(self, post_id, comment_response):
        comment = Comment()
        comment.comment_id = comment_response.get('id')
        comment.created_time = comment_response.get('created_time', None)
        comment.from_id = comment_response.get('from', {}).get('id')
        comment.message = comment_response.get('message')
        comment.angry_total = comment_response.get('angry', {}).get('summary', {}).get('total_count', 0)
        comment.haha_total = comment_response.get('haha', {}).get('summary', {}).get('total_count', 0)
        comment.like_total = comment_response.get('like', {}).get('summary', {}).get('total_count', 0)
        comment.love_total = comment_response.get('love', {}).get('summary', {}).get('total_count', 0)
        comment.sad_total = comment_response.get('sad', {}).get('summary', {}).get('total_count', 0)
        comment.wow_total = comment_response.get('wow', {}).get('summary', {}).get('total_count', 0)
        comment.post_id = post_id
        comment.save()
        return comment

    def parse_post(self, post_response, *args, **kwargs):
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