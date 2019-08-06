from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

class InstagramProfile(SoftDeleteMixin, CreateUpdateMixin):
    insta_uid=models.CharField(max_length=255, primary_key=True)
    app_user=models.ForeignKey(User, on_delete=models.CASCADE)
    access_token=models.CharField(max_length=255)
    full_name=models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    is_business = models.BooleanField(default=False)


class InstagramMediaInsight(SoftDeleteMixin, CreateUpdateMixin):
    media_insight_id=models.CharField(max_length=255, primary_key=True)
    insta_user_id=models.ForeignKey(InstagramProfile, on_delete=models.CASCADE)
    likes_count=models.IntegerField(default=0)
    comments_count=models.IntegerField(default=0)
    media_tags=models.CharField(max_length=255, blank=True)
    media_caption = models.TextField(blank=True)
    media_type=models.CharField(max_length=255)
    people_tagged=models.CharField(max_length=255, blank=True)
    filter_used=models.CharField(max_length=255, blank=True)
    post_created_time=models.DateTimeField(default=timezone.now,blank=True)


class InstagramUserMedia(SoftDeleteMixin, CreateUpdateMixin):
    media_id=models.CharField(max_length=255, primary_key=True)
    insta_user_id=models.ForeignKey(InstagramProfile, on_delete=models.CASCADE)
    media_insight_id=models.ForeignKey(InstagramMediaInsight, on_delete=models.CASCADE)
    media_url=models.CharField(max_length=255)