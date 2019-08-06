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
    access_token = models.TextField(null=True, blank=False)
    expires_in = models.IntegerField(null=True, blank=False)
    facebook_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=False)
    last_name = models.CharField(max_length=255, null=True, blank=False)

    class Meta:
        verbose_name = 'Facebook Profile'
        verbose_name_plural = 'Facebook Profiles'

    def __str__(self):
        return self.first_name + " " + self.last_name

class Page(SoftDeleteMixin, CreateUpdateMixin):
    access_token = models.TextField(null=True, blank=False)
    displayed_message_response_time = models.CharField(max_length=255, null=True, blank=False)
    num_engagements = models.IntegerField('total engagements', null=True, blank=False)
    fan_count = models.IntegerField(null=True, blank=False)
    name = models.CharField(max_length=255, null=True, blank=False)
    overall_star_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=False)
    page_consumptions = models.IntegerField(null=True, blank=False)
    page_engaged_users = models.IntegerField(null=True, blank=False)
    page_id = models.CharField(max_length=255)
    page_impressions = models.IntegerField(null=True, blank=False)
    page_impressions_nonviral = models.IntegerField(null=True, blank=False)
    page_impressions_nonviral_unique = models.IntegerField(null=True, blank=False)
    page_impressions_organic = models.IntegerField(null=True, blank=False)
    page_impressions_organic_unique = models.IntegerField(null=True, blank=False)
    page_impressions_paid = models.IntegerField(null=True, blank=False)
    page_impressions_paid_unique = models.IntegerField(null=True, blank=False)
    page_impressions_unique = models.IntegerField(null=True, blank=False)
    page_impressions_viral = models.IntegerField(null=True, blank=False)
    page_impressions_viral_unique = models.IntegerField(null=True, blank=False)
    page_negative_feedback = models.IntegerField(null=True, blank=False)
    page_negative_feedback_unique = models.IntegerField(null=True, blank=False)
    page_post_engagements = models.IntegerField(null=True, blank=False)
    page_video_views = models.IntegerField(null=True, blank=False)
    page_views_total = models.IntegerField(null=True, blank=False)
    rating_count = models.IntegerField(null=True, blank=False)
    talking_about_count = models.IntegerField(null=True, blank=False)
    unread_message_count = models.IntegerField(null=True, blank=False)
    unread_notif_count = models.IntegerField('unread notification count', null=True, blank=False)
    unseen_message_count = models.IntegerField(null=True, blank=False)
    verification_status = models.CharField(max_length=255, null=True, blank=False)

    facebook_profile = models.ForeignKey(FacebookProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RecommendationChoice(Enum):
    negative = 'negative'
    none = 'none'
    positive = 'positive'

    @classmethod
    def get_recommendation_choices(cls):
        return [(recommendation.value, recommendation.value.title()) for recommendation in RecommendationChoice]

class Rating(SoftDeleteMixin, CreateUpdateMixin):
    created_time = models.DateTimeField()
    rating = models.SmallIntegerField(null=True, blank=True)
    recommendation_type = models.CharField(max_length=8, choices=RecommendationChoice.get_recommendation_choices())
    review_text = models.TextField(null=True, blank=True)

    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_text

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
        return [(reaction.value, reaction.value.title()) for reaction in ReactionChoice]

class PostReaction(SoftDeleteMixin, CreateUpdateMixin):
    from_id = models.CharField(max_length=255)
    reaction_type = models.CharField(max_length=5, choices=ReactionChoice.get_reaction_choices())

    class Meta:
        verbose_name = 'Post Reaction'
        verbose_name_plural = 'Post Reactions'

    def __str__(self):
        return self.reaction_type

class TimelineVisibilityChoice(Enum):
    HIDDEN = 'HIDDEN'
    NORMAL = 'NORMAL'
    FORCED_ALLOW = 'FORCED_ALLOW'

    @classmethod
    def get_timeline_visibility_choices(cls):
        return [(timeline_visibility.value, timeline_visibility.value.replace('_', ' ').title()) for timeline_visibility in TimelineVisibilityChoice]

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
    timeline_visibility = models.CharField(max_length=12, choices=TimelineVisibilityChoice.get_timeline_visibility_choices())
    updated_time = models.DateTimeField()

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    reactions = models.ManyToManyField('PostReaction', blank=True)

    def __str__(self):
        return self.message or self.story or self.post_id

class CommentReaction(SoftDeleteMixin, CreateUpdateMixin):
    from_id = models.CharField(max_length=255)
    reaction_type = models.CharField(max_length=5, choices=ReactionChoice.get_reaction_choices())

    class Meta:
        verbose_name = 'Comment Reaction'
        verbose_name_plural = 'Comment Reactions'

    def __str__(self):
        return self.reaction_type

class Comment(SoftDeleteMixin, CreateUpdateMixin):
    comment_id = models.CharField(max_length=255)
    created_time = models.DateTimeField()
    from_id = models.CharField(max_length=255)
    message = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reactions = models.ManyToManyField('CommentReaction', blank=True)

    def __str__(self):
        return self.message