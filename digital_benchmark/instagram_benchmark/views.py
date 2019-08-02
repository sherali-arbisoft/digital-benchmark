from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import View, generic
import requests
import json
from urllib.request import urlopen
from .models import InstagramProfile


# index view is temporary, leaving it as function based view that's why
def index(request):
    return HttpResponse('instagram benchmark app is up!')

class AuthView(generic.ListView):
    #model = User
    template_name = 'auth.html'

    def get_queryset(self):
        return
# def auth(request):
#     return render(request,'auth.html',{})

class LoginSuccessView(View):
    def get(self, request):
        instaCode=request.GET['code']
        print(instaCode)
        data={
                'client_id':'4d8f538893ba481f88c0614865dc9310',
                'client_secret':'8e2bba68038844ab8e240b7094db18f2',
                'grant_type': 'authorization_code',
                'redirect_uri':'http://127.0.0.1:8000/instagram_benchmark/login_success',
                'code':instaCode
            }
        response = requests.post(url='https://api.instagram.com/oauth/access_token', data=data,headers={'Content-Type': 'application/x-www-form-urlencoded'})

        userdata=response.json()
        #print(userdata)
        newIgUser=InstagramProfile(insta_uid=userdata['user']['id'],app_user_id=request.user.id,access_token=userdata['access_token'],full_name=userdata['user']['full_name'],username=userdata['user']['username'],is_business=userdata['user']['is_business'])
        newIgUser.save()
        return render(request,'firstpage.html',{'data':userdata})

def login(request):
    url="https://api.instagram.com/oauth/authorize/?client_id=4d8f538893ba481f88c0614865dc9310&redirect_uri=http://127.0.0.1:8000/instagram_benchmark/login_success&response_type=code"

    return redirect(url)