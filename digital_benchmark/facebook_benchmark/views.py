from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response

from datetime import datetime

import requests 

from .forms import LoginForm
from .data_provider import FacebookUserDataProvider, FacebookPageDataProvider
from .data_parser import FacebookUserDataParser, FacebookPageDataParser
from .models import FacebookProfile, Page, Post
from .serializers import FacebookProfileSerializer, PageSerializer, PostSerializer
from .permissions import PageAccessPermission, PostAccessPermission
from .tasks import FetchPostsTask
from .login import FacebookLogin

@method_decorator(login_required, name='dispatch')
class LoginView(View):
    def get(self, request, *args, **kwargs):
        try:
            facebook_profile = request.user.facebook_profile
            facebook_login = FacebookLogin()
            inspect_user_access_token_response = facebook_login.inspect_access_token(facebook_profile.access_token)
            if not facebook_login.is_access_token_valid(inspect_user_access_token_response):
                raise Http404('Facebook User Access Token is not Valid.')
            if facebook_login.rerequest(inspect_user_access_token_response):
                return redirect(settings.FACEBOOK_REREQUEST_SCOPE_URL)
            else:
                return redirect('/facebook_benchmark/home')
        except FacebookProfile.DoesNotExist:
            context = {
                'facebook_login_url': settings.FACEBOOK_LOGIN_URL,
            }
            return render(request, 'facebook_benchmark/login.html', context)

@method_decorator(login_required, name='dispatch')
class LoginSuccessfulView(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            raise Http404('Facebook Login Code not Found.')
        facebook_login = FacebookLogin()
        user_access_token = facebook_login.get_access_token_from_code(code)
        inspect_user_access_token_response = facebook_login.inspect_access_token(user_access_token)
        if not facebook_login.is_access_token_valid(inspect_user_access_token_response):
            raise Http404('Facebook User Access Token is not Valid.')
        if facebook_login.rerequest(inspect_user_access_token_response):
            return redirect(settings.FACEBOOK_REREQUEST_SCOPE_URL)
        facebook_user_data_provider = FacebookUserDataProvider(user_access_token=user_access_token)
        profile_response = facebook_user_data_provider.get_profile()
        if 'error' in profile_response:
            raise Http404('Facebook User Profile not Found.')
        facebook_user_data_parser = FacebookUserDataParser(user_id=request.user.id)
        facebook_profile = facebook_user_data_parser.parse_profile(profile_response, user_access_token, facebook_login.get_data_access_expires_at(inspect_user_access_token_response))
        
        pages_response = facebook_user_data_provider.get_pages()
        if 'error' in pages_response:
            raise Http404('Facebook User Pages not Found.')
        pages = facebook_user_data_parser.parse_pages(pages_response)
        for page in pages:
            page_access_token = facebook_login.get_long_term_token(page.access_token)
            inspect_page_access_token_response = facebook_login.inspect_access_token(page_access_token)
            if not facebook_login.is_access_token_valid(inspect_page_access_token_response):
                raise Http404('Facebook User Page Access Token is not Valid.')
            page.access_token = page_access_token
            page.expires_at = facebook_login.get_data_access_expires_at(inspect_page_access_token_response)
            page.save()

        return redirect('/facebook_benchmark/home')

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        try:
            facebook_profile = request.user.facebook_profile
            all_pages = Page.objects.filter(facebook_profile=facebook_profile)
            context = {
                'all_pages': all_pages,
            }
            return render(request, 'facebook_benchmark/home.html', context)
        except FacebookProfile.DoesNotExist:
            raise Http404("Facebook Profile does not Exist.")

@method_decorator(login_required, name='dispatch')
class LoadPageDataView(View):
    def get(self, request, page_id, *args, **kwargs):
        page = get_object_or_404(Page, facebook_profile=request.user.facebook_profile, pk=page_id)
        fetch_posts_task = FetchPostsTask
        fetch_posts_task.delay(page.access_token, page.facebook_profile_id, page.id)
        return redirect('/facebook_benchmark/home')

class FacebookProfileDetail(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FacebookProfileSerializer

    def get_queryset(self):
        return FacebookProfile.objects.filter(user=self.request.user)

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
        return Post.objects.filter(page__facebook_profile__user=self.request.user).prefetch_related('comments')

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

    def get_queryset(self):
        return Post.objects.filter(page_id=self.kwargs.get('page_id'), page__facebook_profile__user=self.request.user).order_by('-created_at').prefetch_related('comments')

class PostRevisionsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(post_id=self.kwargs.get('post_id'), page__facebook_profile__user=self.request.user).order_by('-created_at').prefetch_related('comments')

class PostLatestRevision(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        try:
            post = [Post.objects.filter(post_id=self.kwargs.get('post_id'), page__facebook_profile__user=self.request.user).latest('-created_at')]
        except Post.DoesNotExist:
            post = Post.objects.none()
        return post