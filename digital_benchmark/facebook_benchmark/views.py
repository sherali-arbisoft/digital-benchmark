from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings

import requests

from .forms import LoginForm, LoadDataForm
from .data_provider import FacebookUserDataProvider, FacebookPageDataProvider
from .data_parser import FacebookUserDataParser, FacebookPageDataParser
from .models import FacebookProfile, Page

# Create your views here.
class LoginView(View):
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'facebook_benchmark/login.html', context)
    
    def post(self, request, *args, **kwargs):
        url = settings.FACEBOOK_LOGIN_URL
        return redirect(url)

class LoginSuccessfulView(View):
    def get(self, request):
        url = settings.FACEBOOK_ACCESS_TOKEN_URL
        data = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.FACEBOOK_LOGIN_SUCCESSFUL_REDIRECT_URI,
            'client_secret': settings.FACEBOOK_APP_SECRET,
            'code': request.GET['code'],
        }
        response = requests.post(url, data=data).json()

        facebook_user_data_provider = FacebookUserDataProvider(user_access_token=response.get('access_token', ''))
        profile_response = facebook_user_data_provider.get_profile()

        facebook_user_data_parser = FacebookUserDataParser()
        facebook_profile = facebook_user_data_parser.parse_profile(profile_response)
        
        facebook_profile.access_token = response.get('access_token', '')
        facebook_profile.expires_in = response.get('expires_in', 0)
        facebook_profile.save()

        request.session['facebook_profile_id'] = facebook_profile.id
        
        all_pages_response = facebook_user_data_provider.get_all_pages()
        all_pages = facebook_user_data_parser.parse_all_pages(all_pages_response)

        for page in all_pages:
            url = settings.FACEBOOK_ACCESS_TOKEN_URL
            data = {
                'grant_type': settings.FACEBOOK_GRANT_TYPE,
                'client_id': settings.FACEBOOK_APP_ID,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'fb_exchange_token': page.access_token
            }
            response = requests.post(url, data=data).json()
            page.access_token = response.get('access_token', '')
            page.save()

        return redirect('/facebook_benchmark/home')

class HomeView(View):
    def get(self, request, *args, **kwargs):
        facebook_profile_id = request.session.get('facebook_profile_id', '')
        all_pages = Page.objects.filter(facebook_profile_id=facebook_profile_id)
        context = {
            'all_pages': all_pages,
        }
        return render(request, 'facebook_benchmark/home.html', context)
    
    def post(self, request, *args, **kwargs):
        facebook_profile_id = request.session.get('facebook_profile_id', '')

        pages = Page.objects.filter(facebook_profile_id=facebook_profile_id)

        for page in pages:
            facebook_page_data_provider = FacebookPageDataProvider(page_access_token=page.access_token)
            facebook_page_data_parser = FacebookPageDataParser()
            
            page_details_response = facebook_page_data_provider.get_page_details()
            page_insights_response = facebook_page_data_provider.get_page_insights()
            
            facebook_page_data_parser.parse_page_details_and_insights(facebook_profile_id, page, page_details_response, page_insights_response)
            
            posts_details_and_insights_response = facebook_page_data_provider.get_all_posts_details_and_insights()

            facebook_page_data_parser.parse_all_posts_details_and_insights(page.id, posts_details_and_insights_response)

        context = {
            'success_message': 'Data Loaded Successfully.'
        }
        return render(request, 'facebook_benchmark/home.html', context)

class LoadPageDataView(View):
    def get(self, request, page_id, *args, **kwargs):
        facebook_profile_id = request.session.get('facebook_profile_id', '')
        page = get_object_or_404(Page, pk=page_id)
        facebook_page_data_provider = FacebookPageDataProvider(page_access_token=page.access_token)
        facebook_page_data_parser = FacebookPageDataParser(facebook_profile_id=facebook_profile_id, page_id=page_id)
        
        page_details_response = facebook_page_data_provider.get_page_details()
        page_insights_response = facebook_page_data_provider.get_page_insights()
        
        facebook_page_data_parser.parse_page_details(page_details_response)
        facebook_page_data_parser.parse_page_insights(page_insights_response)

        all_posts_response = facebook_page_data_provider.get_all_posts()
        all_posts = facebook_page_data_parser.parse_all_posts(all_posts_response=all_posts_response)
        
        all_pages = Page.objects.filter(facebook_profile_id=facebook_profile_id)
        context = {
            'success_message': 'Page Data Loaded Successfully.',
            'all_pages': all_pages,
        }
        return render(request, 'facebook_benchmark/home.html', context)