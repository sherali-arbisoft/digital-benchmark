# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings
import psycopg2
from django.utils import timezone
time_now = timezone.now()
settings = get_project_settings()


class InstagramPipeline(object):

    def __init__(self):
        self.crawler_id = None
        self.insta_uid = None
        self.media_count = None

    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=settings.get('HOSTNAME'), user=settings.get(
            'USERNAME'), password=settings.get('PASSWORD'), dbname=settings.get('DB_NAME'))
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        if self.insta_uid and self.media_count and self.crawler_id:
            self._update_spider_db_record()
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.crawler_id = item.get('unique_id')
        self.insta_uid = item.get('insta_uid')
        self.media_count = item.get('media_count')
        insta_user_id = 0
        profile = self._get_user_from_db(item.get('insta_uid'),item.get('django_auth_user'))
        if profile:
            insta_user_id = profile[0]
        elif item.get('_type') == "profile":
            self._parse_profile(item)
        if item.get('_type') == "media":
            self._parse_media(item, insta_user_id)
        elif item.get('_type') == "comment":
            self._parse_comment(item)
        return item

    def _get_user_from_db(self, insta_uid, app_user_id):
        existing_user_query = f"select * from instagram_benchmark_instagramprofile where insta_uid='{insta_uid}' and app_user_id='{app_user_id}'"
        self.cursor.execute(existing_user_query)
        profile = self.cursor.fetchone()
        return profile

    def _fetch_current_media(self, insta_media_id):
        existing_media_query = f"select * from instagram_benchmark_instagramusermedia where media_id='{insta_media_id}'"
        self.cursor.execute(existing_media_query)
        media = self.cursor.fetchone()
        return media

    def _update_spider_db_record(self):
        running_spider_query = f"update instagram_benchmark_crawlerstats set status='Completed',user_scrapped='{self.insta_uid}',no_of_media_scrapped={self.media_count}  where unique_id='{self.crawler_id}';"
        self.cursor.execute(running_spider_query)
        try:
            self.connection.commit()
        except Exception as e:
            print('Exception while updating crawlerstats table')
            raise e

    def _parse_profile(self, item):
        query = f"insert into instagram_benchmark_instagramprofile(insta_uid,is_active,created_at,last_updated_at,app_user_id,access_token,full_name,username,follows_count,folowed_by_count,media_count,is_business) values({item.get('insta_uid')},{True},'{time_now}','{time_now}',{item.get('django_auth_user')},'n/a','{item.get('full_name')}','{item.get('username')}',{item.get('follows_count')},{item.get('folowed_by_count')},{item.get('media_count')},{item.get('is_business')});"
        self.cursor.execute(query)
        try:
            self.connection.commit()
        except Exception as e:
            print('exception while saving scraped profile to postgres')
            raise e

    def _parse_media(self, item, insta_user_id):
        media_insight_id = 0
        self.cursor.execute("insert into instagram_benchmark_instagrammediainsight(insta_user_id,is_active,created_at,last_updated_at,likes_count,comments_count,media_tags,media_caption,media_type,people_tagged,filter_used,post_created_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
                            (insta_user_id, True, time_now, time_now, item.get('likes_count'), item.get('comments_count'), item.get('media_tags'), item.get('media_caption'), item.get('media_type'), item.get('people_tagged'), item.get('filter_used'), item.get('post_created_time')))
        media_insight_id = self.cursor.fetchone()[0]
        try:
            self.connection.commit()
        except Exception as e:
            print('exception while saving scraped media_insight to postgres')
            raise e

        self.cursor.execute("insert into instagram_benchmark_instagramusermedia(insta_user_id,is_active,created_at,last_updated_at,media_id,media_url,media_insight_id,crawler_id) values(%s,%s,%s,%s,%s,%s,%s,%s);",
                            (insta_user_id, True, time_now, time_now, item.get('media_id'), item.get('media_url'), media_insight_id, self.crawler_id))
        try:
            self.connection.commit()
        except Exception as e:
            print('exception while saving scraped media to postgres')
            raise e

    def _parse_comment(self, item):
        insta_media_id = item.get('media_id')
        media = self._fetch_current_media(insta_media_id)
        media_unique_id = media[0]
        self.cursor.execute("insert into instagram_benchmark_instagrammediacomments(is_active,created_at,last_updated_at,comment_id,media_id,comment_text,comment_by) values(%s,%s,%s,%s,%s,%s,%s);",
                            (True, time_now, time_now, item.get('comment_id'), media_unique_id, item.get('comment_text'), item.get('comment_by')))
        try:
            self.connection.commit()
        except Exception as e:
            print('exception while saving scraped comment to postgres')
            raise e
