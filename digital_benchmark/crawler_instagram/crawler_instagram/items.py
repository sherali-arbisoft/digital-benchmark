# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class InstagramProfileItem(Item):
    insta_uid=Field()
    full_name=Field()
    username=Field()
    follows_count=Field()
    folowed_by_count=Field()
    media_count=Field()
    is_business = Field()
    _type=Field()
    django_auth_user=Field()
    unique_id=Field()


class InstagramMediaItem(Item):
    media_id=Field()
    media_url=Field()
    likes_count=Field()
    comments_count=Field()
    media_tags=Field()
    media_caption = Field()
    media_type=Field()
    people_tagged=Field()
    filter_used=Field()
    post_created_time=Field()
    _type=Field()
    insta_uid=Field()
    unique_id=Field()
    media_count=Field()

class InstagramCommentItem(Item):
    comment_id=Field()
    media_id=Field()
    comment_text=Field()
    comment_by=Field()
    insta_uid=Field()
    unique_id=Field()
    media_count=Field()
    _type=Field()