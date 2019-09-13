from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, JsonResponse

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import datetime

import requests

from .data_provider import FacebookUserDataProvider, FacebookPageDataProvider
from .data_parser import FacebookUserDataParser, FacebookPageDataParser
from .models import FacebookProfile, Page, Post
from .serializers import FacebookProfileSerializer, PageSerializer, PostSerializer
from .permissions import PageAccessPermission, PostAccessPermission
from .tasks import FetchPostsTask
from .utils import FacebookLoginUtils

@method_decorator(login_required, name='dispatch')
class LoginView(View):
    def get(self, request):
        try:
            FacebookLoginUtils.inspect_access_token(request.user.facebook_profile.access_token)
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
        user_access_token = FacebookLoginUtils.get_access_token(code)
        FacebookLoginUtils.inspect_access_token(user_access_token)
        facebook_user_data_provider = FacebookUserDataProvider(user_access_token=user_access_token)
        profile_response = facebook_user_data_provider.get_profile()
        facebook_user_data_parser = FacebookUserDataParser(user_id=request.user.id)
        facebook_profile = facebook_user_data_parser.parse_profile(profile_response, user_access_token, FacebookLoginUtils.get_data_access_expires_at(user_access_token))
        return redirect('/facebook_benchmark/home')

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        try:
            facebook_profile = request.user.facebook_profile
            facebook_user_data_provider = FacebookUserDataProvider(facebook_profile.access_token)
            accounts_response = facebook_user_data_provider.get_accounts()
            for account_response in accounts_response:
                page_access_token = FacebookLoginUtils.get_long_term_token(account_response.get('access_token'))
                FacebookLoginUtils.inspect_access_token(page_access_token)
                facebook_page_data_provider = FacebookPageDataProvider(page_access_token)
                page_response = facebook_page_data_provider.get_page()
                facebook_page_data_parser = FacebookPageDataParser(facebook_profile_id=facebook_profile.id)
                page = facebook_page_data_parser.parse_page(page_response, page_access_token, FacebookLoginUtils.get_data_access_expires_at(page_access_token))
            pages = Page.objects.filter(facebook_profile=facebook_profile)
            context = {
                'pages': pages,
            }
            return render(request, 'facebook_benchmark/home.html', context)
        except FacebookProfile.DoesNotExist:
            return redirect('/facebook_benchmark/login')

@method_decorator(login_required, name='dispatch')
class LoadPageDataView(View):
    def get(self, request, page_id):
        page = get_object_or_404(Page, facebook_profile=request.user.facebook_profile, pk=page_id)
        FetchPostsTask.delay(page.access_token, page.facebook_profile_id, page.id)
        return redirect('/facebook_benchmark/home')

class FetchFacebookProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_access_token):
        user_access_token = FacebookLoginUtils.get_long_term_token(user_access_token)
        facebook_user_data_provider = FacebookUserDataProvider(user_access_token=user_access_token)
        profile_response = facebook_user_data_provider.get_profile()
        facebook_user_data_parser = FacebookUserDataParser(user_id=request.user.id)
        facebook_profile = facebook_user_data_parser.parse_profile(profile_response, user_access_token, FacebookLoginUtils.get_data_access_expires_at(user_access_token))
        return JsonResponse(FacebookProfileSerializer(facebook_profile).data)

class FacebookProfileDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FacebookProfileSerializer

    def retrieve(self, request, pk=None):
        try:
            facebook_profile = request.user.facebook_profile
            serializer = self.get_serializer(facebook_profile)
            return Response(serializer.data)
        except FacebookProfile.DoesNotExist:
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

class PostLatestRevision(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def retrieve(self, request, post_id=None):
        try:
            post = Post.objects.filter(post_id=post_id, page__facebook_profile__user=self.request.user).latest('-created_at')
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'detail': 'Not found.'})