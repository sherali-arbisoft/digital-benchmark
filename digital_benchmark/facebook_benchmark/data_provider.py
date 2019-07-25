import facebook as fb
import requests

from django.conf import settings

class FacebookDataProvider:
    def __init__(self, page_access_token, *args, **kwargs):
        self.page_access_token = page_access_token
        self.graph_api_client = fb.GraphAPI(access_token=page_access_token, version=settings.FACEBOOK_GRAPH_API_VERSION)
    
    def get_page_details(self, fields=''):
        if not fields:
            fields = settings.FACEBOOK_DEFAULT_FIELDS_FOR_PAGE
        page = self.graph_api_client.get_object(id='me', fields=fields)
        return page
    
    def get_all_posts(self, fields=''):
        if not fields:
            fields = settings.FACEBOOK_DEFAULT_FIELDS_FOR_FEED
        feed = self.graph_api_client.get_connections(id='me', connection_name='feed', fields=fields)
        all_posts = feed['data']
        while 'paging' in feed and 'next' in feed['paging']:
            feed = requests.get(feed['paging']['next']).json()
            if feed['data']:
                all_posts += feed['data']
        return all_posts
    
    def get_post_details(self, post_id, fields=''):
        if not fields:
            fields = settings.FACEBOOK_DEFAULT_FIELDS_FOR_POST
        post = self.graph_api_client.get_object(id=post_id, fields=fields)
        return post
    
    def get_page_insights(self, metrices=''):
        if not metrices:
            metrices = settings.FACEBOOK_DEFAULT_METRICES_FOR_PAGE_INSIGHTS
        page_insights = self.graph_api_client.get_connections(id='me', connection_name='insights', metric=metrices)
        return page_insights
    
    def get_post_insights(self, post_id, metrices=''):
        if not metrices:
            metrices = settings.FACEBOOK_DEFAULT_METRICES_FOR_POST_INSIGHTS
        post_insights = self.graph_api_client.get_connections(id=post_id, connection_name='insights', metric=metrices)
        return post_insights