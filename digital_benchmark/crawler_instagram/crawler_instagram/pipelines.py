# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import datetime
time_now=datetime.datetime.utcnow()


class InstagramPipeline(object):

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'benchmarkAppDB'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cursor = self.connection.cursor()
    
    def close_spider(self, spider):
        running_spider_query="update instagram_benchmark_crawlerstats set status='Completed',user_scrapped='{}',no_of_media_scrapped={}  where unique_id='{}'".format(self.insta_uid,self.media_count,self.unique_id_of_crawler_instance)
        self.cursor.execute(running_spider_query)
        try:
            self.connection.commit()
            print('crawler_stats table updated successfully')
        except Exception as e:
            print('Exception while updating crawlerstats table')
            raise e
        
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.unique_id_of_crawler_instance=item.get('unique_id')
        self.insta_uid=item.get('insta_uid')
        self.media_count=item.get('media_count')
        existing_user_query="select * from instagram_benchmark_instagramprofile where insta_uid='{}'".format(item.get('insta_uid'))
        self.cursor.execute(existing_user_query)
        profile=self.cursor.fetchone()
        insta_user_id=profile[0]
        if item.get('_type')=="profile":
            if profile:
                pass
            else:
                self.cursor.execute("insert into instagram_benchmark_instagramprofile(insta_uid,is_active,created_at,last_updated_at,app_user_id,access_token,full_name,username,follows_count,folowed_by_count,media_count,is_business) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                (item.get('insta_uid'),True,time_now,time_now,item.get('django_auth_user'),'n/a',item.get('full_name'),item.get('username'),item.get('follows_count'),item.get('folowed_by_count'),item.get('media_count'),item.get('is_business')))
                try:
                    self.connection.commit()    
                except Exception as e:
                    print('exception while saving scraped profile to postgres')
                    raise e
        
        elif item.get('_type')=="media":
            media_insight_id=0
            self.cursor.execute("insert into instagram_benchmark_instagrammediainsight(insta_user_id,is_active,created_at,last_updated_at,likes_count,comments_count,media_tags,media_caption,media_type,people_tagged,filter_used,post_created_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",
            (insta_user_id,True,time_now,time_now,item.get('likes_count'),item.get('comments_count'),item.get('media_tags'),item.get('media_caption'),item.get('media_type'),item.get('people_tagged'),item.get('filter_used'),item.get('post_created_time')))
            media_insight_id=self.cursor.fetchone()[0]
            try:
                self.connection.commit()    
            except Exception as e:
               print('exception while saving scraped media_insight to postgres')
               raise e

            self.cursor.execute("insert into instagram_benchmark_instagramusermedia(insta_user_id,is_active,created_at,last_updated_at,media_id,media_url,media_insight_id) values(%s,%s,%s,%s,%s,%s,%s);",
            (insta_user_id,True,time_now,time_now,item.get('media_id'),item.get('media_url'),media_insight_id))
            try:
                self.connection.commit()    
            except Exception as e:
               print('exception while saving scraped media to postgres')
               raise e
        
        elif item.get('_type')=="comment":
            insta_media_id=item.get('media_id')
            existing_media_query="select * from instagram_benchmark_instagramusermedia where media_id='{}'".format(insta_media_id)
            self.cursor.execute(existing_media_query)
            media=self.cursor.fetchone()
            media_unique_id=media[0]
            self.cursor.execute("insert into instagram_benchmark_instagrammediacomments(is_active,created_at,last_updated_at,comment_id,media_id,comment_text,comment_by) values(%s,%s,%s,%s,%s,%s,%s);",
            (True,time_now,time_now,item.get('comment_id'),media_unique_id,item.get('comment_text'),item.get('comment_by')))
            try:
                self.connection.commit()    
            except Exception as e:
               print('exception while saving scraped comment to postgres')
               raise e

        return item
