from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View, generic
from requests_oauthlib import OAuth1Session



class LoginView(generic.ListView):
    template_name = 'Login/index.html'

    def get_queryset(self):
        return


class AuthView(View):
    def get(self,request):
        oauth = OAuth1Session(settings.CONSUMER_KEY, client_secret=settings.CONSUMER_SECRET)
        fetch_response = oauth.fetch_request_token(settings.REQUEST_TOKEN_URL)
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        print("Got OAuth token: %s" % resource_owner_key)
        print("Got OAuth token: %s" % resource_owner_secret)
        authorization_url = oauth.authorization_url(settings.BASE_AUTHORIZATION_URL)
        print(authorization_url)
        return redirect(authorization_url)



class SuccessView(View):
    def get(self,request):
        return render(request, 'success/index.html')


