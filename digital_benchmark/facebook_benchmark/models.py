from django.db import models
from django.utils import timezone

from enum import Enum

class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

class FacebookProfile(SoftDeleteMixin, CreateUpdateMixin):
    access_token = models.TextField()
    expires_in = models.IntegerField()
    facebook_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

class Brand(SoftDeleteMixin, CreateUpdateMixin):
    name = models.CharField(max_length=255)

class Page(SoftDeleteMixin, CreateUpdateMixin):
    access_token = models.TextField()
    displayed_message_response_time = models.CharField(max_length=255)
    num_engagements = models.IntegerField()
    fan_count = models.IntegerField()
    name = models.CharField(max_length=255)
    overall_start_rating = models.SmallIntegerField(null=True)
    page_consumptions = models.IntegerField()
    page_engaged_users = models.IntegerField()
    page_id = models.CharField(max_length=255)
    page_impressions = models.IntegerField()
    page_impressions_nonviral = models.IntegerField()
    page_impressions_nonviral_unique = models.IntegerField()
    page_impressions_organic = models.IntegerField()
    page_impressions_organic_unique = models.IntegerField()
    page_impressions_paid = models.IntegerField()
    page_impressions_paid_unique = models.IntegerField()
    page_impressions_unique = models.IntegerField()
    page_impressions_viral = models.IntegerField()
    page_impressions_viral_unique = models.IntegerField()
    page_negative_feedback = models.IntegerField()
    page_negative_feedback_unique = models.IntegerField()
    page_post_engagements = models.IntegerField()
    page_video_views = models.IntegerField()
    page_views_total = models.IntegerField()
    rating_count = models.IntegerField()
    talking_about_count = models.IntegerField()
    unread_message_count = models.IntegerField()
    unread_notif_count = models.IntegerField()
    unseen_message_count = models.IntegerField()
    verification_status = models.CharField(max_length=255)

    facebook_profile = models.ForeignKey(FacebookProfile, on_delete=models.CASCADE)

class ReactionChoice(Enum):
    angry = 'ANGRY'
    haha = 'HAHA'
    like = 'LIKE'
    love = 'LOVE'
    none = 'NONE'
    sad = 'SAD'
    wow = 'WOW'

    @classmethod
    def get_reaction_choices(self):
        return [(reaction.value, reaction) for reaction in ReactionChoice]

class PostReaction(SoftDeleteMixin, CreateUpdateMixin):
    from_id = models.CharField(max_length=255)
    reaction_type = models.CharField(max_length=5, choices=ReactionChoice.get_reaction_choices())

class Post(SoftDeleteMixin, CreateUpdateMixin):
    backdated_time = models.DateTimeField(null=True)
    created_time = models.DateTimeField()
    is_eligible_for_promotion = models.BooleanField()
    is_expired = models.BooleanField()
    is_hidden = models.BooleanField()
    is_instagram_eligible = models.BooleanField()
    is_popular = models.BooleanField()
    is_published = models.BooleanField()
    message = models.TextField(null=True)
    post_clicks = models.IntegerField()
    post_clicks_unique = models.IntegerField()
    post_engaged_fan = models.IntegerField()
    post_engaged_users = models.IntegerField()
    post_id = models.CharField(max_length=255)
    post_impressions = models.IntegerField()
    post_impressions_fan = models.IntegerField()
    post_impressions_fan_paid = models.IntegerField()
    post_impressions_fan_paid_unique = models.IntegerField()
    post_impressions_fan_unique = models.IntegerField()
    post_impressions_nonviral = models.IntegerField()
    post_impressions_nonviral_unique = models.IntegerField()
    post_impressions_organic = models.IntegerField()
    post_impressions_organic_unique = models.IntegerField()
    post_impressions_paid = models.IntegerField()
    post_impressions_paid_unique = models.IntegerField()
    post_impressions_unique = models.IntegerField()
    post_impressions_viral = models.IntegerField()
    post_impressions_viral_unique = models.IntegerField()
    post_negative_feedback = models.IntegerField()
    post_negative_feedback_unique = models.IntegerField()
    promotion_status = models.CharField(max_length=255)
    scheduled_publish_time = models.DateTimeField(null=True)
    shares = models.IntegerField()
    story = models.TextField(null=True)
    timeline_visibility = models.CharField(max_length=255)
    updated_time = models.DateTimeField()

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    reactions = models.ManyToManyField('PostReaction', blank=True)

class CommentReaction(SoftDeleteMixin, CreateUpdateMixin):
    from_id = models.CharField(max_length=255)
    reaction_type = models.CharField(max_length=5, choices=ReactionChoice.get_reaction_choices())

class Comment(SoftDeleteMixin, CreateUpdateMixin):
    comment_id = models.CharField(max_length=255)
    created_time = models.DateTimeField()
    from_id = models.CharField(max_length=255)
    message = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reactions = models.ManyToManyField('CommentReaction', blank=True)