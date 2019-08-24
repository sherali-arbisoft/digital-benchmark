import requests

from django.conf import settings

class InstagramDataProvider:

    def __init__(self, access_token, *args, **kwargs):
        self.access_token = access_token

    def get_user_profile(self):
        url=settings.PROFILE_URL.format(self.access_token)
        response = requests.get(url=url)
        profile_data=response.json()
        return profile_data

    def get_user_media(self):
        all_media=[]
        url=settings.RECENT_MEDIA_URL.format(self.access_token)
        response = requests.get(url=url)
        recent_media=response.json()
        all_media+=recent_media['data']
        while True:
            if 'next_url'  not in recent_media['pagination']:
                break
            else:
                recent_media = self._get_next_media(recent_media['pagination']['next_url'])
                all_media+=recent_media['data']
        return all_media
    
    def _get_next_media(self, next_url):
        return requests.get(next_url).json()
    
    def get_media_comments(self, media_id):
        all_comments=[]
        url=settings.COMMENTS_URL.format(media_id,self.access_token)
        response = requests.get(url=url)
        recent_comments=response.json()
        return recent_comments['data']