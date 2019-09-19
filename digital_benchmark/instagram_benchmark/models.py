from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SoftDeleteMixin(models.Model):
    """ 
     This is a class for all database records to indicate if they are active of destroyed.
    """
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class CreateUpdateMixin(models.Model):
    """ 
      This is a class for all database records to auto add creation and updation time.
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class InstagramProfile(SoftDeleteMixin, CreateUpdateMixin):
    insta_uid = models.CharField(max_length=255)
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    follows_count = models.IntegerField(default=0)
    folowed_by_count = models.IntegerField(default=0)
    media_count = models.IntegerField(default=0)
    is_business = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class InstagramMediaInsight(SoftDeleteMixin, CreateUpdateMixin):
    insta_user = models.ForeignKey(InstagramProfile, on_delete=models.CASCADE)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    media_tags = models.TextField(default="")
    media_caption = models.TextField(default="")
    media_type = models.CharField(max_length=255)
    people_tagged = models.CharField(max_length=255, default="")
    filter_used = models.CharField(max_length=255, default="")
    post_created_time = models.DateTimeField(default=timezone.now, blank=True)


class InstagramUserMedia(SoftDeleteMixin, CreateUpdateMixin):
    media_id = models.CharField(max_length=255)
    insta_user = models.ForeignKey(InstagramProfile, on_delete=models.CASCADE)
    media_insight = models.ForeignKey(
        InstagramMediaInsight, related_name='urls', on_delete=models.CASCADE)
    media_url = models.TextField(default="")
    crawler_id = models.TextField(default="")

    def __str__(self):
        return self.media_url


class InstagramMediaComments(SoftDeleteMixin, CreateUpdateMixin):
    comment_id = models.CharField(max_length=255)
    media = models.ForeignKey(
        InstagramUserMedia, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField(default="")
    comment_by = models.TextField(default="")


class CrawlerStats(SoftDeleteMixin, CreateUpdateMixin):
    task_id = models.CharField(max_length=255)
    unique_id = models.CharField(max_length=255, primary_key=True)
    status = models.CharField(max_length=255)
    user_scrapped = models.CharField(max_length=255)
    no_of_media_scrapped = models.IntegerField(default=0)
