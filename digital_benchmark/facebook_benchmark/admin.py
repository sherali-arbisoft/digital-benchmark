from django.contrib import admin

from .models import Page, Post

# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass