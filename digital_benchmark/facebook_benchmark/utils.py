from django.conf import settings
from django.http import Http404
from django.utils.timezone import make_aware
import requests
from datetime import datetime

from .middleware import redirect

class FacebookLoginUtils:
    @staticmethod
    def inspect_access_token(access_token):
        access_token_inspection_response = FacebookLoginUtils.get_access_token_inspection(access_token)
        FacebookLoginUtils.access_token_validation(access_token_inspection_response)
        FacebookLoginUtils.rerequest(access_token_inspection_response)

    @staticmethod
    def get_access_token_inspection(access_token):
        inspect_access_token_url_data = {
            'input_token': access_token,
            'access_token': settings.FACEBOOK_APP_TOKEN,
        }
        return requests.get(settings.FACEBOOK_INSPECT_ACCESS_TOKEN_URL, params=inspect_access_token_url_data).json()
    
    @staticmethod
    def get_data_access_expires_at(access_token):
        access_token_inspection_response = FacebookLoginUtils.get_access_token_inspection(access_token)
        return make_aware(datetime.utcfromtimestamp(access_token_inspection_response.get('data', {}).get('data_access_expires_at', 0)))

    @staticmethod
    def get_scopes(access_token_inspection_response):
        return access_token_inspection_response.get('data', {}).get('scopes')

    @staticmethod
    def access_token_validation(inspect_access_token_response):
        if not inspect_access_token_response.get('data', {}).get('is_valid', False):
            raise Http404("Access Token is not Valid.")
    
    @staticmethod
    def is_access_token_valid(access_token):
        access_token_inspection_response = FacebookLoginUtils.get_access_token_inspection(access_token)
        return access_token_inspection_response.get('data', {}).get('is_valid', False)

    @staticmethod
    def rerequest(access_token_inspection_response):
        for scope in settings.FACEBOOK_SCOPE:
            scopes = FacebookLoginUtils.get_scopes(access_token_inspection_response)
            if scope not in scopes:
                print(True)
                return redirect(settings.FACEBOOK_REREQUEST_SCOPE_URL)
    
    @staticmethod
    def get_access_token(code):
        access_token_url_data = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': code,
        }
        access_token_response = requests.post(settings.FACEBOOK_ACCESS_TOKEN_URL, data=access_token_url_data).json()
        return access_token_response.get('access_token')
    
    @staticmethod
    def get_long_term_token(short_term_token):
        access_token_url_data = {
            'grant_type': settings.FACEBOOK_GRANT_TYPE,
            'client_id': settings.FACEBOOK_APP_ID,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'fb_exchange_token': short_term_token,
        }
        access_token_response = requests.post(settings.FACEBOOK_ACCESS_TOKEN_URL, data=access_token_url_data).json()
        return access_token_response.get('access_token')