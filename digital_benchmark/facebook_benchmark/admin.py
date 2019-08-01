from django.contrib import admin

from .models import Page, Post

# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_engagements', 'fan_count', 'unread_message_count', 'unread_notif_count', 'verification_status')

    list_filter = ['verification_status']

    search_fields = ['name']

    date_hierarchy = 'created_at'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass