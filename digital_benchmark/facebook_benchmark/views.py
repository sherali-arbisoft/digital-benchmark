from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import generics

import requests

from .forms import LoginForm
from .data_provider import FacebookUserDataProvider, FacebookPageDataProvider
from .data_parser import FacebookUserDataParser, FacebookPageDataParser
from .models import FacebookProfile, Page, Post
from .serializers import FacebookProfileSerializer, PageSerializer, PostSerializer

@method_decorator(login_required, name='dispatch')
class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'facebook_login_url': settings.FACEBOOK_LOGIN_URL,
        }
        return render(request, 'facebook_benchmark/login.html', context)

@method_decorator(login_required, name='dispatch')
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

        facebook_user_data_parser = FacebookUserDataParser(user_id=request.user.id)
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

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        facebook_profile_id = request.session.get('facebook_profile_id', '')
        all_pages = Page.objects.filter(facebook_profile_id=facebook_profile_id)
        context = {
            'all_pages': all_pages,
        }
        return render(request, 'facebook_benchmark/home.html', context)

@method_decorator(login_required, name='dispatch')
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
        
        messages.success(request, 'Page Data Loaded Successfully.')
        messages.info(request, f"{len(all_posts)} Posts Added.")
        messages.info(request, f"{sum([len(post.comment_set.all()) for post in all_posts ])} Comments Added.")
        messages.info(request, f"{sum([len(post.reactions.all()) for post in all_posts ])} Post Reactions Added.")
        return redirect('/facebook_benchmark/home')

class FacebookProfileList(generics.ListAPIView):
    serializer_class = FacebookProfileSerializer

    def get_queryset(self):
        return FacebookProfile.objects.filter(user=self.request.user)

class PageList(generics.ListAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        facebook_profile = FacebookProfile.objects.get(user=self.request.user)
        return Page.objects.filter(facebook_profile=facebook_profile)

class PostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        page = Page.objects.get(id=self.kwargs.get('id', ''))
        return Post.objects.filter(page=page)

class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()