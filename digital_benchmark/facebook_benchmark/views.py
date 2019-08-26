from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response

import requests

from .forms import LoginForm
from .data_provider import FacebookUserDataProvider, FacebookPageDataProvider
from .data_parser import FacebookUserDataParser, FacebookPageDataParser
from .models import FacebookProfile, Page, Post
from .serializers import FacebookProfileSerializer, PageSerializer, PostSerializer
from .permissions import PageAccessPermission, PostAccessPermission

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
        messages.info(request, f"{sum([len(post.comments.all()) for post in all_posts ])} Comments Added.")
        messages.info(request, f"{sum([len(post.reactions.all()) for post in all_posts ])} Post Reactions Added.")
        return redirect('/facebook_benchmark/home')

class FacebookProfileDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FacebookProfileSerializer

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = FacebookProfile.objects.filter(user=self.request.user)
        if queryset:
            serializer = self.get_serializer(queryset[0])
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not found.'})

class PageList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']

    def get_queryset(self):
        return Page.objects.filter(facebook_profile__user=self.request.user)

class PageDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, PageAccessPermission]
    serializer_class = PageSerializer
    queryset = Page.objects.all()

class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(page__facebook_profile__user=self.request.user)

class PostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, PostAccessPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class PagePostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message', 'story', 'comments__message', 'reactions__reaction_type', 'comments__reactions__reaction_type']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['message', 'story']
    
    def list(self, request, page_id=None, *args, **kwargs):
        queryset = Post.objects.filter(page_id=page_id, page__facebook_profile__user=self.request.user).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PostRevisionsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def list(self, request, post_id=None, *args, **kwargs):
        queryset = Post.objects.filter(post_id=post_id, page__facebook_profile__user=self.request.user).order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PostLatestRevision(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def retrieve(self, request, post_id=None, *args, **kwargs):
        queryset = Post.objects.filter(post_id=post_id, page__facebook_profile__user=self.request.user).order_by('-created_at')
        if queryset:
            serializer = self.get_serializer(queryset[0])
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not found.'})