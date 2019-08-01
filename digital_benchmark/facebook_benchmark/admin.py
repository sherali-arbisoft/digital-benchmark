from django.contrib import admin

from .models import Brand, Page, Post, PostReaction, Comment, CommentReaction

# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']

    date_hierarchy = 'created_at'

    empty_value_display = '--empty--'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_engagements', 'fan_count', 'unread_message_count', 'unread_notif_count', 'verification_status')

    list_filter = ['verification_status']

    search_fields = ['name']

    date_hierarchy = 'created_at'

    empty_value_display = '--empty--'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'story')

    search_fields = ['message', 'story']

    date_hierarchy = 'created_time'

    empty_value_display = '--empty--'

@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ('from_id', 'get_reaction_type_display')

    search_fields = ['from_id', 'reaction_type']

    empty_value_display = '--empty--'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('from_id', 'message')

    search_fields = ['from_id','message']

    date_hierarchy = 'created_time'

    empty_value_display = '--empty--'

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('from_id', 'get_reaction_type_display')

    search_fields = ['from_id', 'reaction_type']

    empty_value_display = '--empty--'