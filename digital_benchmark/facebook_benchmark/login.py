from django.conf import settings
import requests

class FacebookLogin:
    def inspect_access_token(self, access_token, *args, **kwargs):
        inspect_access_token_url_data = {
            'input_token': access_token,
            'access_token': settings.FACEBOOK_APP_TOKEN,
        }
        return requests.get(settings.FACEBOOK_INSPECT_ACCESS_TOKEN_URL, params=inspect_access_token_url_data).json()

    def is_access_token_valid(self, inspect_access_token_response, *args, **kwargs):
        return inspect_access_token_response.get('data', {}).get('is_valid', False)
    
    def rerequest(self, inspect_access_token_response, *args, **kwargs):
        for scope in settings.FACEBOOK_SCOPE:
            scopes = inspect_access_token_response.get('data', {}).get('scopes')
            if scope not in scopes:
                return True
        return False