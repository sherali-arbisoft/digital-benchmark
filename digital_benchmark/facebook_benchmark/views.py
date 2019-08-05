from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

import requests

from .forms import LoginForm
from .data_provider import FacebookUserDataProvider
from .data_parser import FacebookUserDataParser

# Create your views here.
class LoginView(View):
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'facebook_benchmark/login.html', context)
    
    def post(self, request, *args, **kwargs):
        url = 'https://www.facebook.com/v{version}/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={permissions}&response_type={response_type}&state={state}'.format(version=settings.FACEBOOK_GRAPH_API_VERSION, app_id=settings.FACEBOOK_APP_ID, redirect_uri=settings.FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI, permissions=','.join(settings.FACEBOOK_PERMISSIONS), response_type=settings.FACEBOOK_RESPONSE_TYPE, state=settings.FACEBOOK_STATE)
        return redirect(url)

class LoginSuccessfulView(View):
    def get(self, request):
        url = 'https://graph.facebook.com/v{version}/oauth/access_token'.format(version=settings.FACEBOOK_GRAPH_API_VERSION)
        data = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': request.GET['code'],
        }
        response = requests.post(url, data=data).json()

        facebook_user_data_provider = FacebookUserDataProvider(user_access_token=response.get('access_token', ''))
        facebook_profile_response = facebook_user_data_provider.get_profile()

        facebook_user_data_parser = FacebookUserDataParser()
        facebook_profile = facebook_user_data_parser.parse_profile(facebook_profile_response)
        
        facebook_profile.access_token = response.get('access_token', '')
        facebook_profile.expires_in = response.get('expires_in', 0)
        facebook_profile.save()
        
        all_pages_response = facebook_user_data_provider.get_all_pages()
        all_pages = facebook_user_data_parser.parse_all_pages(facebook_profile.id, all_pages_response)

        for page in all_pages:
            url = 'https://graph.facebook.com/v{version}/oauth/access_token'.format(version=settings.FACEBOOK_GRAPH_API_VERSION)
            data = {
                'grant_type': settings.FACEBOOK_GRANT_TYPE,
                'client_id': settings.FACEBOOK_APP_ID,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'fb_exchange_token': page.access_token
            }
            response = requests.post(url, data=data).json()
            page.access_token = response.get('access_token', '')
        
        return redirect('/facebook_benchmark/home')

class HomeView(View):
    def get(self, request):
        return render(request, 'facebook_benchmark/home.html')