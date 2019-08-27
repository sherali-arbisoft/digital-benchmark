from facebook import GraphAPI, GraphAPIError
import requests

from django.conf import settings

class FacebookUserDataProvider:
    def __init__(self, user_access_token, *args, **kwargs):
        self.user_access_token = user_access_token
        self.graph_api_client = GraphAPI(access_token=user_access_token, version=settings.FACEBOOK_GRAPH_API_VERSION)
    
    def get_profile(self, fields='', *args, **kwargs):
        fields = fields or ','.join(settings.FACEBOOK_DEFAULT_FIELDS_FOR_PROFILE)
        profile = self.graph_api_client.get_object(id='me', fields=fields)
        return profile
    
    def get_all_pages(self, fields='', *args, **kwargs):
        fields = fields or ','.join(settings.FACEBOOK_DEFAULT_FIELDS_FOR_ACCOUNTS)
        all_pages = self.graph_api_client.get_connections(id='me', connection_name='accounts', fields=fields)
        return all_pages

class FacebookPageDataProvider:
    def __init__(self, page_access_token, *args, **kwargs):
        self.page_access_token = page_access_token 
        self.graph_api_client = GraphAPI(access_token=page_access_token, version=settings.FACEBOOK_GRAPH_API_VERSION)
    
    def get_object_response(self, id, fields):
        try:
            return self.graph_api_client.get_object(id=id, fields=fields)
        except GraphAPIError as e:
            return e.result
    
    def get_connection_response(self, id, connection_name, fields):
        try:
            responses = self.graph_api_client.get_all_connections(id=id, connection_name=connection_name, fields=fields)
            return [response for response in responses]
        except GraphAPIError as e:
            return e.result

    def get_page(self, *args, **kwargs):
        return self.get_object_response(settings.FACEBOOK_OBJECT_SELF, ','.join(settings.FACEBOOK_PAGE_DEFAULT_FIELDS))

    def get_page_rating(self, *args, **kwargs):
        return self.get_connection_response(settings.FACEBOOK_OBJECT_SELF, settings.FACEBOOK_CONNECTION_RATINGS, ','.join(settings.FACEBOOK_PAGE_RATING_DEFAULT_FIELDS))
    
    def get_post_reactions(self, post_id, *args, **kwargs):
        return self.get_connection_response(post_id, settings.FACEBOOK_CONNECTION_REACTIONS, ','.join(settings.FACEBOOK_PAGE_POST_REACTIONS_DEFAULT_FIELDS))
    
    def get_post_comments(self, post_id, *args, **kwargs):
        return self.get_connection_response(post_id, settings.FACEBOOK_CONNECTION_COMMENTS, ','.join(settings.FACEBOOK_PAGE_POST_COMMENTS_DEFAULT_FIELDS))

    def get_post_comment_reactions(self, comment_id, *args, **kwargs):
        return self.get_connection_response(comment_id, settings.FACEBOOK_CONNECTION_REACTIONS, ','.join(settings.FACEBOOK_PAGE_POST_COMMENT_REACTIONS_DEFAULT_FIELDS))
    
    def get_post(self, post_id, *args, **kwargs):
        return self.get_object_response(post_id, ','.join(settings.FACEBOOK_PAGE_POST_DEFAULT_FIELDS))

    def get_posts(self, *args, **kwargs):
        return self.get_connection_response(settings.FACEBOOK_OBJECT_SELF, settings.FACEBOOK_CONNECTION_POSTS, ','.join(settings.FACEBOOK_PAGE_POST_DEFAULT_FIELDS))