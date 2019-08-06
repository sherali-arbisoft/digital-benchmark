from django.contrib import admin

# Register your models here.

from .models import InstagramProfile,InstagramUserMedia,InstagramMediaInsight,InstagramMediaComments

#admin.site.register([InstagramProfile,InstagramUserMedia,InstagramMediaInsight,InstagramMediaComments])

@admin.register(InstagramProfile)
class InstagramProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'is_business')

    list_filter = ['is_business']

    search_fields = ['username', 'full_name']
    
    date_hierarchy = 'created_at'

    empty_value_display = '--empty--'


@admin.register(InstagramUserMedia)
class InstagramUserMediaAdmin(admin.ModelAdmin):
    list_display = ('media_id', 'media_url')

    list_filter = ['created_at']

    search_fields = ['media_id']
    
    date_hierarchy = 'created_at'

    empty_value_display = '--empty--'


@admin.register(InstagramMediaInsight)
class InstagramMediaInsightAdmin(admin.ModelAdmin):
    list_display = ('post_created_time', 'likes_count', 'comments_count','media_tags','media_caption','media_type','filter_used')

    list_filter = ['post_created_time','likes_count','media_type']

    search_fields = ['media_tags', 'media_caption']
    
    date_hierarchy = 'created_at'

    empty_value_display = '--empty--'


@admin.register(InstagramMediaComments)
class InstagramMediaCommentsAdmin(admin.ModelAdmin):
    list_display = ('media', 'comment_text', 'comment_by')

    list_filter = ['comment_by']

    search_fields = ['comment_text', 'comment_by']
    
    date_hierarchy = 'created_at'

    empty_value_display = '--empty--'