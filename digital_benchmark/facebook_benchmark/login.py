from django.conf import settings
import requests
from datetime import datetime

class FacebookLogin:
    def inspect_access_token(self, access_token, *args, **kwargs):
        inspect_access_token_url_data = {
            'input_token': access_token,
            'access_token': settings.FACEBOOK_APP_TOKEN,
        }
        return requests.get(settings.FACEBOOK_INSPECT_ACCESS_TOKEN_URL, params=inspect_access_token_url_data).json()
    
    def get_data_access_expires_at(self, inspect_access_token_response, *args, **kwargs):
        return datetime.utcfromtimestamp(inspect_access_token_response.get('data', {}).get('data_access_expires_at', 0))

    def is_access_token_valid(self, inspect_access_token_response, *args, **kwargs):
        return inspect_access_token_response.get('data', {}).get('is_valid', False)
    
    def rerequest(self, inspect_access_token_response, *args, **kwargs):
        for scope in settings.FACEBOOK_SCOPE:
            scopes = inspect_access_token_response.get('data', {}).get('scopes')
            if scope not in scopes:
                return True
        return False
    
    def get_access_token_from_code(self, code, *args, **kwargs):
        access_token_url_data = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }
        access_token_response = requests.post(settings.FACEBOOK_ACCESS_TOKEN_URL, data=access_token_url_data).json()
        return access_token_response.get('access_token')
    
    def get_long_term_token(self, short_term_token, *args, **kwargs):
        access_token_url_data = {
            'grant_type': settings.FACEBOOK_GRANT_TYPE,
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'fb_exchange_token': short_term_token,
        }
        access_token_response = requests.post(settings.FACEBOOK_ACCESS_TOKEN_URL, data=access_token_url_data).json()
        return access_token_response.get('access_token')