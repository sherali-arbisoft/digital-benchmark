from .serializers import InstagramProfileSerializer, InstagramUserMediaSerializer, InstagramMediaCommentsSerializer
from rest_framework import generics, filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View, generic
import requests
import json
from urllib.request import urlopen
from .models import InstagramProfile, CrawlerStats, InstagramMediaInsight, InstagramUserMedia, InstagramMediaComments
from .data_parser import InstagramDataParser
from .data_provider import InstagramDataProvider
from django.conf import settings
from django.contrib import messages
from rest_framework.views import APIView

from scrapyd_api import ScrapydAPI
from uuid import uuid4
# connect scrapyd service
scrapyd = ScrapydAPI(settings.SCRAPYD_SERVER_URL)


class InstagramProfileList(generics.ListAPIView):
    serializer_class = InstagramProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return InstagramProfile.objects.filter(app_user=user)


class InstagramMediaList(generics.ListAPIView):
    serializer_class = InstagramUserMediaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = InstagramProfile.objects.filter(app_user=user)
        query_set = InstagramUserMedia.objects.select_related(
            'media_insight').prefetch_related('comments').filter(insta_user=profile[0])
        return query_set


class InstagramMediaRevisionList(generics.ListAPIView):
    serializer_class = InstagramUserMediaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        media_id = self.kwargs.get('media_id')
        user = self.request.user
        profile = InstagramProfile.objects.filter(app_user=user)
        query_set = InstagramUserMedia.objects.select_related('media_insight').prefetch_related(
            'comments').filter(insta_user=profile[0], media_id=media_id)
        return query_set


class MediaRevisionDetail(generics.RetrieveAPIView):
    serializer_class = InstagramUserMediaSerializer
    permission_classes = [IsAuthenticated]
    queryset = InstagramUserMedia.objects.select_related(
        'media_insight').prefetch_related('comments').all()


class MediaRevisionComments(generics.ListAPIView):
    serializer_class = InstagramMediaCommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = InstagramProfile.objects.filter(app_user=user)
        revision_id = self.kwargs.get('revision_id')
        media = InstagramUserMedia.objects.filter(
            insta_user=profile[0], id=revision_id)
        if media:
            return media[0].comments.all()
        return media


class AuthView(generic.ListView):
    template_name = 'auth.html'

    def get_queryset(self):
        return


class InstagramUserDataLoad(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_token = request.data.get('access_token')
        user_id = request.user.id
        self._load_data(access_token, user_id)
        return Response({"Success": "User data fetched and saved successfully"})

    def _load_data(self, access_token, user_id):
        dataProvider, instagram_parser, current_profile = self._load_profile(
            access_token, user_id)
        self._load_media(dataProvider, instagram_parser,
                         current_profile, access_token)

    def _load_profile(self, access_token, user_id):
        dataProvider = InstagramDataProvider(access_token)
        instagram_parser = InstagramDataParser()
        user_profile_data = dataProvider.get_user_profile().get('data')
        current_profile = InstagramProfile.objects.filter(
            insta_uid=user_profile_data.get('id'), app_user_id=user_id).first()
        if current_profile:
            current_profile.access_token = access_token
            current_profile.save()
        else:
            new_profile = instagram_parser.save_profile_data(
                user_profile_data, user_id, access_token)
            current_profile = new_profile
        return dataProvider, instagram_parser, current_profile

    def _load_media(self, dataProvider, instagram_parser, current_user, access_token):
        all_user_media = dataProvider.get_user_media()
        instagram_parser.save_media_insight_data(
            all_user_media, current_user, access_token)


class ConnectionSuccessView(View):
    def get(self, request):
        instaCode = request.GET['code']
        data = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'grant_type': settings.GRANT_TYPE,
            'redirect_uri': settings.INSTA_REDIRECT_URL,
            'code': instaCode
        }
        response = requests.post(url=settings.INSTA_FETCH_USER_URL, data=data, headers={
                                 'Content-Type': 'application/x-www-form-urlencoded'})
        userdata = response.json()
        try:
            this_user = InstagramProfile.objects.get(
                insta_uid=userdata['user']['id'], app_user_id=request.user.id)
            this_user.access_token = userdata['access_token']
            this_user.save()
            messages.success(
                request, 'Instagram account connected successfully')
        except InstagramProfile.DoesNotExist:
            app_user_id = request.user.id
            instagram_parser = InstagramDataParser()
            this_user = instagram_parser.parse_save_profile_data(
                userdata, app_user_id)
            messages.success(request, 'Instagram account {} connected successfully'.format(
                this_user.username))
        return render(request, 'firstpage.html', {'messages': messages.get_messages(request), 'insta_id': userdata['user']['id']})


class FetchUserDataView(View):
    def get(self, request, insta_id=None):
        try:
            current_user = InstagramProfile.objects.get(
                app_user_id=request.user.id, insta_uid=insta_id)
            access_token = current_user.access_token
            insta_uid = current_user.insta_uid
            dataProvider = InstagramDataProvider(access_token)
            instagram_parser = InstagramDataParser()
            # fetch profile
            user_profile_data = dataProvider.get_user_profile().get('data')
            current_profile = InstagramProfile.objects.get(insta_uid=insta_uid)
            message = instagram_parser.save_profile_update(
                user_profile_data, current_profile)
            if message:
                messages.success(request, message)
            # fetch media
            all_user_media = dataProvider.get_user_media()
            # parse media insight and data
            data_save_message = instagram_parser.save_media_insight_data(
                all_user_media, current_user, access_token)
            for message in data_save_message:
                messages.success(request, message)
            return render(request, 'mediafetched.html', {'messages': messages.get_messages(request)})
        except InstagramProfile.DoesNotExist:
            print('current user not connected to instagram!')
            messages.info(
                request, 'Logout instagram account from browser and connect it again')
            return render(request, 'auth.html', {'messages': messages.get_messages(request)})
        except Exception as e:
            print('exception while fetching and saving instagram user media')
            raise e
        return render(request, 'firstpage.html', {'data': {}})


class InstaConnectView(View):
    def post(self, request):
        if request.user.id:
            url = settings.INSTA_CONNECT_URL
            return redirect(url)
        else:
            return redirect(settings.DJANGO_LOGIN_URL)

        return render(request, 'auth.html')


class InstaCrawlerView(View):
    def post(self, request):
        app_user_id = request.user.id
        unique_id = str(uuid4())
        public_username = request.POST['username']
        setting = {
            'unique_id': unique_id,
            'USER_AGENT': settings.SCRAPER_AGENT
        }
        crawler_triggered = self._trigger_crawler(
            setting, public_username, unique_id, app_user_id)
        if crawler_triggered:
            messages.success(
                request, 'Instagram crawler triggered from scrapy')
            return render(request, 'auth.html', {'messages': messages.get_messages(request)})
        return render(request, 'auth.html', {'messages': "Error in triggering crawler"})

    def _trigger_crawler(self, settings, public_username, unique_id, app_user_id):
        task = scrapyd.schedule('default', 'insta_crawler', settings=settings,
                                username=public_username, unique_id=unique_id, django_user_id=app_user_id)
        crawler_stats = CrawlerStats()
        crawler_stats.unique_id = unique_id
        crawler_stats.task_id = task
        crawler_stats.status = "Started"
        try:
            crawler_stats.save()
            return True
        except:
            return False
