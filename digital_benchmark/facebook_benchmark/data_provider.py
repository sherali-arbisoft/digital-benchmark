from facebook import GraphAPI, GraphAPIError
import requests

from django.conf import settings

class FacebookDataProvider:
    def __init__(self, access_token, *args, **kwargs):
        self.access_token = access_token
        self.graph_api_client = GraphAPI(access_token=access_token, version=settings.FACEBOOK_GRAPH_API_VERSION)
    
    def _get_object_response(self, id, fields):
        try:
            return self.graph_api_client.get_object(id=id, fields=fields)
        except GraphAPIError as e:
            return e.result
    
    def _get_connection_response(self, id, connection_name, fields):
        try:
            responses = self.graph_api_client.get_all_connections(id=id, connection_name=connection_name, fields=fields)
            return [response for response in responses]
        except GraphAPIError as e:
            return e.result


class FacebookUserDataProvider(FacebookDataProvider):
    def __init__(self, user_access_token, *args, **kwargs):
        FacebookDataProvider.__init__(self, user_access_token)
    
    def get_profile(self, *args, **kwargs):
        return self._get_object_response(settings.FACEBOOK_OBJECT_SELF, ','.join(settings.FACEBOOK_PROFILE_DEFAULT_FIELDS))
    
    def get_pages(self, *args, **kwargs):
        return self._get_connection_response(settings.FACEBOOK_OBJECT_SELF, settings.FACEBOOK_CONNECTION_ACCOUNTS, ','.join(settings.FACEBOOK_ACCOUNTS_DEFAULT_FIELDS))

class FacebookPageDataProvider(FacebookDataProvider):
    def __init__(self, page_access_token, *args, **kwargs):
        FacebookDataProvider.__init__(self, page_access_token)
    
    def get_page_rating(self, *args, **kwargs):
        return self._get_connection_response(settings.FACEBOOK_OBJECT_SELF, settings.FACEBOOK_CONNECTION_RATINGS, ','.join(settings.FACEBOOK_PAGE_RATING_DEFAULT_FIELDS))

    def get_page(self, *args, **kwargs):
        return self._get_object_response(settings.FACEBOOK_OBJECT_SELF, ','.join(settings.FACEBOOK_PAGE_DEFAULT_FIELDS))
    
    def get_post_comments(self, post_id, *args, **kwargs):
        return self._get_connection_response(post_id, settings.FACEBOOK_CONNECTION_COMMENTS, ','.join(settings.FACEBOOK_PAGE_POST_COMMENTS_DEFAULT_FIELDS))
    
    def get_post(self, post_id, *args, **kwargs):
        return self._get_object_response(post_id, ','.join(settings.FACEBOOK_PAGE_POST_DEFAULT_FIELDS))

    def get_posts(self, *args, **kwargs):
        return self._get_connection_response(settings.FACEBOOK_OBJECT_SELF, settings.FACEBOOK_CONNECTION_POSTS, ','.join(settings.FACEBOOK_PAGE_POST_DEFAULT_FIELDS))