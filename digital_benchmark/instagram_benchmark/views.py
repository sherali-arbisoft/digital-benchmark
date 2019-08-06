from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import View, generic
import requests
import json
from urllib.request import urlopen
from .models import InstagramProfile
from .data_parser import InstagramDataParser
from .data_provider import InstagramDataProvider

from django.contrib import messages


# index view is temporary, leaving it as function based view that's why
def index(request):
    return HttpResponse('instagram benchmark app is up!')

class AuthView(generic.ListView):
    template_name = 'auth.html'

    def get_queryset(self):
        return

class LoginSuccessView(View):
    def get(self, request):
        instaCode=request.GET['code']
        data={
                'client_id':'4d8f538893ba481f88c0614865dc9310',
                'client_secret':'8e2bba68038844ab8e240b7094db18f2',
                'grant_type': 'authorization_code',
                'redirect_uri':'http://127.0.0.1:8000/instagram_benchmark/login_success',
                'code':instaCode
            }
        response = requests.post(url='https://api.instagram.com/oauth/access_token', data=data,headers={'Content-Type': 'application/x-www-form-urlencoded'})
        userdata=response.json()
        try:
            this_user=InstagramProfile.objects.get(insta_uid=userdata['user']['id'],app_user_id=request.user.id)
            this_user.access_token=userdata['access_token']
            this_user.save()
            messages.success(request,'Instagram account connected successfully')
        except InstagramProfile.DoesNotExist:
            app_user_id=request.user.id
            instagram_parser=InstagramDataParser()
            this_user=instagram_parser.parse_profile_data(userdata,app_user_id)
            messages.success(request,'Instagram account connected successfully')
        return render(request,'firstpage.html',{'messages':messages.get_messages(request)})


class FetchDataView(View):
    def get(self, request):
        try:
            this_user=InstagramProfile.objects.get(app_user_id=request.user.id)
            access_token=this_user.access_token
            insta_uid=this_user.insta_uid
            dataProvider1=InstagramDataProvider(access_token)
            all_user_media=dataProvider1.get_user_media()
            #parse media insight and data
            instagram_parser=InstagramDataParser()
            data_save_message=instagram_parser.parse_media_insight_data(all_user_media,this_user,access_token)
            messages.success(request,data_save_message)
            return render(request,'mediafetched.html',{'messages':messages.get_messages(request)})             
        except InstagramProfile.DoesNotExist:
            print('current user not connected to instagram!')
            messages.info(request,'Logout instagram account from browser and connect it again')
            return render(request,'auth.html',{'messages':messages.get_messages(request)})
        except Exception as e:
            print('exception while fetching and saving instagram user media')
            raise e

        return render(request,'firstpage.html',{'data':{}})

def login(request):
    if request.user.id:
        url="https://api.instagram.com/oauth/authorize/?client_id=4d8f538893ba481f88c0614865dc9310&redirect_uri=http://127.0.0.1:8000/instagram_benchmark/login_success&response_type=code&scope=basic+public_content"
        return redirect(url)
    else:
        return redirect('http://127.0.0.1:8000/accounts/login/')