from django.db import models
from django.db import models

from enum import Enum

class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Brand(SoftDeleteMixin):
    name = models.CharField(max_length=255)

class Page(SoftDeleteMixin):
    page_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    displayed_message_response_time = models.CharField(max_length=255)
    engagement = models.IntegerField()
    fan_count = models.IntegerField()
    overall_start_rating = models.SmallIntegerField()
    rating_count = models.IntegerField()
    talking_about_count = models.IntegerField()
    unread_message_count = models.IntegerField()
    unread_notification_count = models.IntegerField()
    unseen_message_count = models.IntegerField()
    verification_status = models.BooleanField()
    page_impressions = models.IntegerField()
    page_engaged_users = models.IntegerField()
    page_consumptions = models.IntegerField()
    page_negative_feedback = models.IntegerField()
    page_fans_online = models.IntegerField()
    page_actions_post_reactions_total = models.IntegerField()
    page_fans = models.IntegerField()
    page_fan_removes = models.IntegerField()
    page_views_total = models.IntegerField()
    page_video_views = models.IntegerField()
    page_posts_impressions = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

class ReactionChoice(Enum):
    NONE = 'None'
    LIKE = 'Like'
    LOVE = 'Love'
    WOW = 'Wow'
    HAHA = 'Haha'
    SAD = 'Sad'
    ANGRY = 'Angry'

class CommentReaction(SoftDeleteMixin):
    from_id = models.CharField(max_length=255)
    reaction_type = models.CharField(max_length=5, choices=[(reaction, reaction.value) for reaction in ReactionChoice])

class Comment(SoftDeleteMixin):
    comment_id = models.CharField(max_length=255)
    message = models.TextField()
    created_time = models.DateTimeField()
    from_id = models.CharField(max_length=255)
    reactions = models.ManyToManyField('CommentReaction', blank=True)

class PostReaction(SoftDeleteMixin):
    from_id = models.CharField(max_length=255)
    reaction_type = models.CharField(max_length=5, choices=[(reaction, reaction.value) for reaction in ReactionChoice])

class Post(SoftDeleteMixin):
    post_id = models.CharField(max_length=255)
    message = models.TextField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    backdated_time = models.DateTimeField()
    scheduled_publish_time = models.DateTimeField()
    is_eligible_for_promotion = models.BooleanField()
    is_instagram_eligible = models.BooleanField()
    is_expired = models.BooleanField()
    is_hidden = models.BooleanField()
    is_popular = models.BooleanField()
    is_published = models.BooleanField()
    promotion_status = models.CharField(max_length=255)
    shares = models.IntegerField()
    story = models.TextField()
    timeline_visibility = models.BooleanField()
    post_impressions = models.IntegerField()
    post_impressions_unique = models.IntegerField()
    post_impressions_fan = models.IntegerField()
    post_impressions_fan_unique = models.IntegerField()
    post_impressions_organic = models.IntegerField()
    post_impressions_organic_unique = models.IntegerField()
    post_impressions_viral = models.IntegerField()
    post_impressions_viral_unique = models.IntegerField()
    post_engaged_users = models.IntegerField()
    post_negative_feedback = models.IntegerField()
    post_negative_feedback_unique = models.IntegerField()
    post_engaged_fan = models.IntegerField()
    post_clicks = models.IntegerField()
    post_clicks_unique = models.IntegerField()
    post_reactions_by_type_total = models.IntegerField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    reactions = models.ManyToManyField('PostReaction', blank=True)