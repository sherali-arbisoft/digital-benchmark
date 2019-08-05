from django.conf import settings

from datetime import datetime

from .models import FacebookProfile, Page, Rating, Post, PostReaction, Comment, CommentReaction

class FacebookUserDataParser:
    def parse_profile(self, profile_response, *args, **kwargs):
        try:
            facebook_profile = FacebookProfile.objects.get(facebook_id=profile_response.get('id', ''))
        except:
            facebook_profile = FacebookProfile()
            facebook_profile.facebook_id = profile_response.get('id', '')
        facebook_profile.first_name = profile_response.get('first_name', '')
        facebook_profile.last_name = profile_response.get('last_name', '')
        return facebook_profile

    def parse_all_pages(self, facebook_profile_id, all_pages_response, *args, **kwargs):
        all_pages = []
        for page_response in all_pages_response['data']:
            try:
                page = Page.objects.get(page_id=page_response.get('id', ''))
            except:
                page = Page()
                page.page_id = page_response.get('id', '')
            page.access_token = page_response.get('access_token', '')
            page.page_id = page_response.get('id', '')
            page.name = page_response.get('name', '')
            page.facebook_profile_id = facebook_profile_id
            all_pages.append(page)
        return all_pages

class FacebookPageDataParser:

    def _set_all_ratings(self, page, page_response):
        for rating_response in page_response['ratings']['data']:
            rating = Rating()
            rating.created_time = rating_response.get('created_time', None)
            rating.rating = rating_response.get('rating', 0)
            rating.recommendation_type = rating_response.get('recommendation_type', 'none')
            rating.review_text = rating_response.get('review_text', '')
            rating.page = page
            rating.save()

    def parse_page_details_and_insights(self, facebook_profile_id, page_response, page_insights_response):
        page = Page()
        page.displayed_message_response_time = page_response.get('displayed_message_response_time', '')
        page.num_engagements = page_response.get('engagement', {}).get('count', 0)
        page.fan_count = page_response.get('fan_count', 0)
        page.name = page_response.get('name', '')
        page.overall_start_rating = page_response.get('overall_start_rating', 0.0)
        page.page_id = page_response.get('id', '')
        page.rating_count = page_response.get('rating_count', 0)
        page.talking_about_count = page_response.get('talking_about_count', 0)
        page.unread_message_count = page_response.get('unread_message_count', 0)
        page.unread_notif_count = page_response.get('unread_notif_count', 0)
        page.unseen_message_count = page_response.get('unseen_message_count', 0)
        page.verification_status = page_response.get('verification_status', 'not_verified')

        for item in page_insights_response['data']:
            setattr(page, item['name'], item['values'][0]['value'])

        page.facebook_profile_id = facebook_profile_id

        page.save()

        if 'ratings' in page_response:
            self._set_all_ratings(page, page_response)

        return page
    
    def _get_all_post_reactions(self, post_response):
        post_reactions = []
        for reaction in post_response['reactions']['data']:
            post_reaction = PostReaction()
            post_reaction.from_id = reaction.get('id', '')
            post_reaction.reaction_type = reaction.get('type', 'NONE')
            post_reaction.save()
            post_reactions.append(post_reaction)
        return post_reactions
    
    def _get_all_comment_reactions(self, comment_response):
        comment_reactions = []
        for reaction in comment_response['reactions']['data']:
            comment_reaction = CommentReaction()
            comment_reaction.from_id = reaction.get('id', '')
            comment_reaction.reaction_type = reaction.get('type', 'NONE')
            comment_reaction.save()
            comment_reactions.append(comment_reaction)
        return comment_reactions
    
    def _set_all_comments(self, post, post_response):
        for comment in post_response['comments']['data']:
            post_comment = Comment()
            post_comment.comment_id = comment.get('id', '')
            post_comment.created_time = comment.get('created_time', None)
            post_comment.from_id = comment.get('id', '')
            post_comment.message = comment.get('message', '')
            post_comment.post_id = post.id
            post_comment.save()
            if 'reactions' in comment:
                comment_reactions = self._get_all_comment_reactions(comment)
                post_comment.reactions.add(*comment_reactions)

    def parse_post_details_and_insights(self, page_id, post_response, post_insights_response):
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
        post.post_id = post_response.get('id', '')
        post.promotion_status = post_response.get('promotion_status', '')
        post.scheduled_publish_time = post_response.get('scheduled_publish_time', None)
        post.shares = post_response.get('shares', {}).get('count', 0)
        post.story = post_response.get('story', None)
        post.timeline_visibility = post_response.get('timeline_visibility', '')
        post.updated_time = post_response.get('updated_time', None)
        for item in post_insights_response['data']:
            setattr(post, item['name'], item['values'][0]['value'])

        post.page_id = page_id

        post.save()

        if 'reactions' in post_response:
            post_reactions = self._get_all_post_reactions(post_response)
            post.reactions.add(*post_reactions)
        
        if 'comments' in post_response:
            self._set_all_comments(post, post_response)

        return post
    
    def parse_all_posts_details_and_insights(self, page_id, all_posts_response):
        all_posts = []
        for post_response in all_posts_response:
            post = self.parse_post_details_and_insights(page_id, post_response, post_response['insights'])
            all_posts.append(post)
        return all_posts