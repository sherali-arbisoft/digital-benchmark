# -*- coding: utf-8 -*-
from crawler_instagram.items import InstagramProfileItem, InstagramMediaItem, InstagramCommentItem
import scrapy
import psycopg2
import json
import requests
import datetime as dt
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class InstagramSpider(scrapy.Spider):
    name = 'insta_crawler'

    def __init__(self, *args, **kwargs):
        self.username_to_crawl = kwargs.get('username')
        self.crawler_id = kwargs.get('unique_id')
        self.django_user_id = kwargs.get('django_user_id')
        self.fetched_media_count = 0

    def start_requests(self):
        url = 'https://www.instagram.com/{}'.format(self.username_to_crawl)
        yield scrapy.Request(url=url, callback=self.parse_ig_user)

    def parse_ig_user(self, response):
        if response.status == 404:
            self._update_crawler_status(self.crawler_id)
        else:
            media_array = []
            response_string = response.css(
                'script::text').re(r'{"config".*')[0]
            response_string = response_string[:-1]
            json_response = json.loads(response_string)
            user_data = json_response.get("entry_data").get(
                "ProfilePage")[0].get("graphql").get("user")

            self.fetched_media_count = user_data.get(
                "edge_owner_to_timeline_media").get("count")

            profile_item = InstagramProfileItem()
            profile_item["_type"] = "profile"
            profile_item["insta_uid"] = user_data.get("id")
            profile_item["full_name"] = user_data.get("full_name")
            profile_item["username"] = user_data.get("username")
            profile_item["is_business"] = user_data.get("is_business_account")
            profile_item["folowed_by_count"] = user_data.get(
                "edge_followed_by").get('count')
            profile_item["follows_count"] = user_data.get(
                "edge_follow").get('count')
            profile_item["media_count"] = self.fetched_media_count
            profile_item["django_auth_user"] = self.django_user_id
            profile_item["unique_id"] = self.crawler_id
            yield profile_item

            media_array = user_data.get(
                "edge_owner_to_timeline_media").get("edges")
            media_count = 0
            has_next_media = user_data.get("edge_owner_to_timeline_media").get(
                "page_info").get("has_next_page")
            insta_id = user_data.get("id")
            while True:
                if has_next_media:
                    media_count = media_count+12
                    end_cursor = user_data.get("edge_owner_to_timeline_media").get(
                        "page_info").get("end_cursor")
                    user_data = self._get_next_media(
                        insta_id, media_count, end_cursor)
                    media_array += user_data.get(
                        "edge_owner_to_timeline_media").get("edges")
                    has_next_media = user_data.get("edge_owner_to_timeline_media").get(
                        "page_info").get("has_next_page")
                else:
                    break
            for media in media_array:
                media = media["node"]
                url = settings.get('MEDIA_URL').format(media["shortcode"])
                yield scrapy.Request(url=url, callback=self.parse_ig_media)

    def _get_next_media(self, user_id, first_media, end_cursor):
        url = settings.get('NEXT_MEDIA_URL').format(
            user_id, first_media, end_cursor)
        response = requests.get(url).json()
        next_media = response.get("data").get("user")
        return next_media

    def parse_ig_media(self, response):
        response_string = response.css('script::text').re(r'{"config".*')[0]
        response_string = response_string[:-1]
        json_response = json.loads(response_string)
        fetched_media = json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]

        media_item = InstagramMediaItem()
        media_item["_type"] = "media"
        media_item["media_id"] = fetched_media.get("id")
        media_item["media_url"] = fetched_media.get("display_url")
        media_item["likes_count"] = fetched_media.get(
            "edge_media_preview_like").get("count")
        if fetched_media.get("edge_media_to_parent_comment", "Not Found") == "Not Found":
            media_item["comments_count"] = 0
        else:
            media_item["comments_count"] = fetched_media.get(
                "edge_media_to_parent_comment").get("count", 0)
        if fetched_media.get("edge_media_to_caption").get("edges"):
            media_item["media_tags"] = fetched_media.get(
                "edge_media_to_caption").get("edges")[0].get("node").get("text")
            media_item["media_caption"] = fetched_media.get(
                "edge_media_to_caption").get("edges")[0].get("node").get("text")
        else:
            media_item["media_tags"] = ""
            media_item["media_caption"] = ""
        media_item["media_type"] = fetched_media.get("__typename")
        media_item["people_tagged"] = len(fetched_media.get(
            "edge_media_to_tagged_user").get("edges"))
        media_item["filter_used"] = "unknown"
        datetime_python = dt.datetime.fromtimestamp(
            int(fetched_media.get("taken_at_timestamp"))).strftime('%Y-%m-%d %H:%M:%S')
        media_item["post_created_time"] = datetime_python
        media_item["insta_uid"] = fetched_media.get("owner").get("id")
        media_item["unique_id"] = self.crawler_id
        media_item["media_count"] = self.fetched_media_count
        media_item["django_auth_user"] = self.django_user_id
        yield media_item

        if fetched_media.get("edge_media_to_parent_comment", "Not Found") != "Not Found":
            comments_array = fetched_media.get(
                "edge_media_to_parent_comment").get("edges")
            for comment in comments_array:
                insta_uid = fetched_media.get("owner").get("id")
                media_id = fetched_media.get("id")
                comment_item = self.parse_ig_media_comment(
                    comment.get('node'), insta_uid, media_id)
                yield comment_item

    def parse_ig_media_comment(self, comment, insta_uid, media_id):
        comment_item = InstagramCommentItem()
        comment_item["comment_id"] = comment.get('id')
        comment_item["media_id"] = media_id
        comment_item["comment_text"] = comment.get('text')
        comment_item["comment_by"] = comment.get('owner').get('id')
        comment_item["_type"] = "comment"
        comment_item["insta_uid"] = insta_uid
        comment_item["unique_id"] = self.crawler_id
        comment_item["media_count"] = self.fetched_media_count
        comment_item["django_auth_user"] = self.django_user_id
        return comment_item

    def _update_crawler_status(self, unique_id):
        self.connection = psycopg2.connect(host=settings.get('HOSTNAME'), user=settings.get(
            'USERNAME'), password=settings.get('PASSWORD'), dbname=settings.get('DB_NAME'))
        self.cursor = self.connection.cursor()
        running_spider_query = f"update instagram_benchmark_crawlerstats set status='Invalid_Profile' where unique_id='{unique_id}';"
        self.cursor.execute(running_spider_query)
        try:
            self.connection.commit()
        except psycopg2.DatabaseError as error:
            print(error)
            print('Exception while updating crawlerstats table')
            raise e
        self.cursor.close()
        self.connection.close()
