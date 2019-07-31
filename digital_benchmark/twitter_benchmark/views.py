from django.shortcuts import render
from django.conf import settings
from django.views import View
from requests_oauthlib import OAuth1Session


class LoginView(View):
    def get(self,request):
        oauth = OAuth1Session(settings.CONSUMER_KEY, client_secret=settings.CONSUMER_SECRET)
        fetch_response = oauth.fetch_request_token(settings.REQUEST_TOKEN_URL)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        print("Got OAuth token: %s" % resource_owner_key)
        print("Got OAuth token: %s" % resource_owner_secret)
        authorization_url = oauth.authorization_url(settings.BASE_AUTHORIZATION_URL)
        print(authorization_url)
        context = {'auth_url': authorization_url}
        return render(request, 'Login/index.html', context)


class SuccessView(View):
    def get(self,request):
        return render(request, 'success/index.html')


