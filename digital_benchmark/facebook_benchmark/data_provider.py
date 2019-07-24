import facebook as fb
import requests

from digital_benchmark.settings import facebook_graph_api_version, facebook_default_fields_for_page

class FacebookDataProvider:
    def __init__(self, page_access_token, *args, **kwargs):
        self.page_access_token = page_access_token
        self.graph = fb.GraphAPI(access_token=page_access_token, version=facebook_graph_api_version)
    
    def get_page_details(self, fields=''):
        if not fields:
            fields = facebook_default_fields_for_page
        page = self.graph.get_object(id='me', fields=fields)
        return page