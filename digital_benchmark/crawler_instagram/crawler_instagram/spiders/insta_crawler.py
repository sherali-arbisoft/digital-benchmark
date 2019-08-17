# -*- coding: utf-8 -*-
import scrapy
import json
import requests
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class InstagramSpider(scrapy.Spider):
    name = 'insta_crawler'
    def start_requests(self):
        #username coming being passed from scrapyd
        start_urls = ['https://www.instagram.com/az_snaps1']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_ig_user)

    def parse_ig_user(self, response):
        media_array=[]
        profile={}
        response_string=response.css('script::text').re(r'{"config".*')[0]
        response_string=response_string[:-1]
        json_response=json.loads(response_string)
        user_data=json_response.get("entry_data").get("ProfilePage")[0].get("graphql").get("user")


        profile["id"]=user_data.get("id")
        profile["full_name"]=user_data.get("full_name")
        profile["username"]=user_data.get("username")
        profile["biography"]=user_data.get("biography")
        profile["is_business"]=user_data.get("is_business_account")
        profile["profile_pic_url"]=user_data.get("profile_pic_url")
        profile["followed_by"]=user_data.get("edge_followed_by")
        profile["following"]=user_data.get("edge_follow")
        profile["media_count"]=user_data.get("edge_owner_to_timeline_media").get("count")
        #yet to save profile data to DB using scrapy pipelines

        media_array=user_data.get("edge_owner_to_timeline_media").get("edges")
        media_count=0
        has_next_media=user_data.get("edge_owner_to_timeline_media").get("page_info").get("has_next_page")
        
        while True:
            has_next_media=user_data.get("edge_owner_to_timeline_media").get("page_info").get("has_next_page")
            if has_next_media:
                media_count=media_count+12
                end_cursor=user_data.get("edge_owner_to_timeline_media").get("page_info").get("end_cursor")
                user_data=self._get_next_media(user_data.get("id"),media_count,end_cursor)
                media_array+=user_data.get("edge_owner_to_timeline_media").get("edges")
            else:
                break
        #following 2 lines temporary
        print('---------------------------------------------------')
        print(len(media_array))
        
        for media in media_array:
            media=media["node"]
            url=settings.get('MEDIA_URL').format(media["shortcode"])
            yield scrapy.Request(url=url, callback=self.parse_ig_media)


    def _get_next_media(self,user_id,first_media,end_cursor):
        url=settings.get('NEXT_MEDIA_URL').format(user_id,first_media,end_cursor)
        response=requests.get(url).json()
        next_media=response.get("data").get("user")
        return next_media
        
    

    def parse_ig_media(self, response):
        media={}
        response_string=response.css('script::text').re(r'{"config".*')[0]
        response_string=response_string[:-1]
        json_response=json.loads(response_string)
        fetched_media=json_response["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
        
        media["id"] = fetched_media.get("id") 
        media["insta_user_id"] = fetched_media.get("owner").get("id")
        media["url"] = fetched_media.get("display_url")
        media["likes_count"] = fetched_media.get("edge_media_preview_like").get("count")
        media["comments_count"] = fetched_media.get("edge_media_to_parent_comment").get("count")
        media["media_tags"] = fetched_media.get("edge_media_to_caption").get("edges")[0].get("node").get("text")
        media["media_caption"] = fetched_media.get("edge_media_to_caption").get("edges")[0].get("node").get("text")
        media["media_type"] = fetched_media.get("__typename")
        media["people_tagged"] = len(fetched_media.get("edge_media_to_tagged_user").get("edges"))
        media["filter_used"] = "unknown"
        #yet to save media data to DB using scrapy pipelines

        comments=fetched_media.get("edge_media_to_parent_comment").get("edges")
        for comment in comments:
            self.parse_ig_media_comment(comment)

        
    def parse_ig_media_comment(self, comment):
        #to be implemented
        #handle single comment and save to DB using scrapy pipelines
        pass