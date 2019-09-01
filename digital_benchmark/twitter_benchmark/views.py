from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View, generic
from requests_oauthlib import OAuth1Session
from .models import AuthToken, UserComment, UserData, OtherTweet, UserTweet
from .data_provider import DataProvider
from .data_parser import TwitterDataParser
from .serializers import UserTweetSerializer, UserDataSerializer, OtherTweetSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
        #ehmadzubair
        data = obj.get_other_tweet('ehmadzubair')
        data = TwitterDataParser.parser_other_tweet(data)
        #print(data)
        return render(request, 'success/index.html')


class UserDataList(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = UserData.objects.filter(app_user=self.request.user)
        serializer = UserDataSerializer(queryset, many=True)
        return Response(serializer.data)


class UserTweetList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTweetSerializer

    def get_queryset(self):
        return UserTweet.objects.filter(app_user_id=self.request.user.id)


class OtherTweetList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OtherTweetSerializer

    def get_queryset(self):
        return OtherTweet.objects.filter(screen_name=self.kwargs.get('screenname'))


class UserTweetByIdList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserTweetSerializer

    def get_queryset(self):
        return UserTweet.objects.filter(tweet_id=self.kwargs.get('id')).order_by('-created_at')


class UserLatestTweet(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, id):
        try:
            queryset = UserTweet.objects.filter(tweet_id=id).latest('created_at')
            serializer = UserTweetSerializer(queryset)
            return Response(serializer.data)
        except UserData.DoesNotExist:
            return Response({'detail': 'Not found.'})


class OtherTweetByIdList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OtherTweetSerializer

    def get_queryset(self):
        return OtherTweet.objects.filter(tweet_id=self.kwargs.get('id')).order_by('-created_at')


class OtherLatestTweet(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, id):
        try:
            queryset = OtherTweet.objects.filter(tweet_id=id).latest('created_at')
            serializer = OtherTweetSerializer(queryset)
            return Response(serializer.data)
        except OtherTweet.DoesNotExist:
            return Response({'detail': 'Not found.'})

