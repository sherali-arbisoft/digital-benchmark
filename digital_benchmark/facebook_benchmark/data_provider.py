import facebook as fb
import requests

from digital_benchmark.settings import facebook_graph_api_version

class FacebookDataProvider:
    def __init__(self, page_access_token, *args, **kwargs):
        self.page_access_token = page_access_token
        self.graph = fb.GraphAPI(access_token=page_access_token, version=facebook_graph_api_version)