from django.conf import settings

from datetime import datetime

from .models import FacebookProfile, Page, Rating, Post, PostReaction, Comment, CommentReaction

class FacebookUserDataParser:
    def __init__(self, user_id, facebook_profile_id=0, *args, **kwargs):
        self.user_id = user_id
        self.facebook_profile_id = facebook_profile_id

    def parse_profile(self, profile_response, *args, **kwargs):
        facebook_profile, created = FacebookProfile.objects.get_or_create(facebook_id=profile_response.get('id', ''), defaults={
            'user_id': self.user_id
        })
        facebook_profile.first_name = profile_response.get('first_name', '')
        facebook_profile.last_name = profile_response.get('last_name', '')
        facebook_profile.user_id = self.user_id
        facebook_profile.save()
        self.facebook_profile_id = facebook_profile.id
        return facebook_profile

    def parse_all_pages(self, all_pages_response, *args, **kwargs):
        all_pages = []
        for page_response in all_pages_response['data']:
            page, created = Page.objects.get_or_create(page_id=page_response.get('id', ''), defaults={
                'facebook_profile_id': self.facebook_profile_id
            })
            page.access_token = page_response.get('access_token', '')
            page.name = page_response.get('name', '')
            all_pages.append(page)
        return all_pages

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
            rating.review_text = rating_response.get('review_text', '')
            rating.page_id = self.page_id
            rating.save()

    def parse_page_details(self, page_details_response, *args, **kwargs):
        page, created = Page.objects.get_or_create(id=self.page_id, defaults={
            'facebook_profile_id': self.facebook_profile_id
        })
        page.displayed_message_response_time = page_details_response.get('displayed_message_response_time', '')
        page.num_engagements = page_details_response.get('engagement', {}).get('count', 0)
        page.fan_count = page_details_response.get('fan_count', 0)
        page.name = page_details_response.get('name', '')
        page.overall_star_rating = page_details_response.get('overall_star_rating', 0.0)
        page.page_id = page_details_response.get('id', '')
        page.rating_count = page_details_response.get('rating_count', 0)
        page.talking_about_count = page_details_response.get('talking_about_count', 0)
        page.unread_message_count = page_details_response.get('unread_message_count', 0)
        page.unread_notif_count = page_details_response.get('unread_notif_count', 0)
        page.unseen_message_count = page_details_response.get('unseen_message_count', 0)
        page.verification_status = page_details_response.get('verification_status', 'not_verified')
        page.save()
        if 'ratings' in page_details_response:
            self._parse_ratings(ratings_response=page_details_response.get('ratings', ''))
        return page
    
    def parse_page_insights(self, page_insights_response, *args, **kwargs):
        page, created = Page.objects.get_or_create(id=self.page_id, defaults={
            'facebook_profile_id': self.facebook_profile_id
        })
        for item in page_insights_response['data']:
            setattr(page, item['name'], item['values'][0]['value'])
        page.save()
        return page
    
    def _get_all_post_reactions(self, post_reactions_response):
        post_reactions = []
        for reaction in post_reactions_response.get('data', ''):
            post_reaction = PostReaction()
            post_reaction.from_id = reaction.get('id', '')
            post_reaction.reaction_type = reaction.get('type', 'NONE')
            post_reaction.save()
            post_reactions.append(post_reaction)
        return post_reactions
    
    def _get_all_comment_reactions(self, comment_reactions_response):
        comment_reactions = []
        for reaction in comment_reactions_response.get('data', ''):
            comment_reaction = CommentReaction()
            comment_reaction.from_id = reaction.get('id', '')
            comment_reaction.reaction_type = reaction.get('type', 'NONE')
            comment_reaction.save()
            comment_reactions.append(comment_reaction)
        return comment_reactions
    
    def _set_all_comments(self, post_id, post_comments_response):
        for comment in post_comments_response.get('data', ''):
            post_comment = Comment()
            post_comment.comment_id = comment.get('id', '')
            post_comment.created_time = comment.get('created_time', None)
            post_comment.from_id = comment.get('from', {}).get('id', '')
            post_comment.message = comment.get('message', '')
            post_comment.post_id = post_id
            post_comment.save()
            if 'reactions' in comment:
                comment_reactions = self._get_all_comment_reactions(comment.get('reactions', ''))
                post_comment.reactions.add(*comment_reactions)
    
    def parse_post_details(self, post_details_response, *args, **kwargs):
        post = Post()
        post.backdated_time = post_details_response.get('backdated_time', None)
        post.created_time = post_details_response.get('created_time', None)
        post.is_eligible_for_promotion = post_details_response.get('is_eligible_for_promotion', False)
        post.is_expired = post_details_response.get('is_expired', False)
        post.is_hidden = post_details_response.get('is_hidden', False)
        post.is_instagram_eligible = post_details_response.get('is_instagram_eligible', False)
        post.is_popular = post_details_response.get('is_popular', False)
        post.is_published = post_details_response.get('is_published', False)
        post.message = post_details_response.get('message', None)
        post.post_id = post_details_response.get('id', '')
        post.promotion_status = post_details_response.get('promotion_status', '')
        post.scheduled_publish_time = post_details_response.get('scheduled_publish_time', None)
        post.shares = post_details_response.get('shares', {}).get('count', 0)
        post.story = post_details_response.get('story', None)
        post.timeline_visibility = post_details_response.get('timeline_visibility', 'NORMAL').upper()
        post.updated_time = post_details_response.get('updated_time', None)
        post.page_id = self.page_id
        post.save()
        if 'reactions' in post_details_response:
            post_reactions = self._get_all_post_reactions(post_details_response.get('reactions', ''))
            post.reactions.add(*post_reactions)
        if 'comments' in post_details_response:
            self._set_all_comments(post.id, post_details_response.get('comments', ''))
        return post
    
    def parse_post_insights(self, post_id, post_insights_response, *args, **kwargs):
        post, created = Post.objects.get_or_create(id=post_id, defaults={
            'page_id': self.page_id
        })
        for item in post_insights_response['data']:
            setattr(post, item['name'], item['values'][0]['value'])
        post.save()
        return post
    
    def parse_all_posts(self, all_posts_response, *args, **kwargs):
        all_posts = []
        for post_response in all_posts_response:
            post = self.parse_post_details(post_response)
            post = self.parse_post_insights(post_id=post.id, post_insights_response=post_response.get('insights', ''))
            all_posts.append(post)
        return all_posts