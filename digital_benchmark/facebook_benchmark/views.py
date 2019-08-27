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
from .tasks import FetchPostsTask

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
        page = get_object_or_404(Page, pk=page_id)
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