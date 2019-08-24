from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View, generic
from requests_oauthlib import OAuth1Session
from .models import AuthToken
from .data_provider import DataProvider
from .data_parser import TwitterDataParser


class LoginView(generic.ListView):
    template_name = 'Login/index.html'

    def get_queryset(self):
        return


class AuthView(View):
    def get(self, request):
        oauth = OAuth1Session(settings.CONSUMER_KEY, client_secret=settings.CONSUMER_SECRET)
        fetch_response = oauth.fetch_request_token(settings.REQUEST_TOKEN_URL)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        authorization_url = oauth.authorization_url(settings.BASE_AUTHORIZATION_URL)
        obj_auth_token = AuthToken()
        obj_auth_token.resource_owner_key = resource_owner_key
        obj_auth_token.resource_owner_secret = resource_owner_secret
        obj_auth_token.save()
        return redirect(authorization_url)


class SuccessView(View):
    def get(self, request):
        obj = DataProvider(request.GET['oauth_verifier'], request.GET['oauth_token'])
        # for testing
        data = obj.get_other_tweet('ehmadzubair')
        #data = TwitterDataParser.parser_other_tweet(data=data)
        print(data)
        return render(request, 'success/index.html')


