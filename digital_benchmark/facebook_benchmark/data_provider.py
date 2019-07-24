import facebook as fb
import requests

from digital_benchmark.settings import facebook_graph_api_version, facebook_default_fields_for_page, facebook_default_fields_for_feed, facebook_default_fields_for_post

class FacebookDataProvider:
    def __init__(self, page_access_token, *args, **kwargs):
        self.page_access_token = page_access_token
        self.graph = fb.GraphAPI(access_token=page_access_token, version=facebook_graph_api_version)
    
    def get_page_details(self, fields=''):
        if not fields:
            fields = facebook_default_fields_for_page
        page = self.graph.get_object(id='me', fields=fields)
        return page
    
    def get_all_posts(self, fields=''):
        if not fields:
            fields = facebook_default_fields_for_feed
        feed = self.graph.get_connections(id='me', connection_name='feed', fields=fields)
        all_posts = feed['data']
        while 'paging' in feed and 'next' in feed['paging']:
            feed = requests.get(feed['paging']['next']).json()
            if feed['data']:
                all_posts += feed['data']
        return all_posts
    
    def get_post_details(self, post_id, fields=''):
        if not fields:
            fields = facebook_default_fields_for_post
        post = self.graph.get_object(id=post_id, fields=fields)
        return post