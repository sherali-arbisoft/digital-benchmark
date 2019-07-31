from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import requests

import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


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

class LoginSuccessView(generic.ListView):
    #model = User
    template_name = 'firstpage.html'

    def get_queryset(self):
        return

def login(request):
    url="https://api.instagram.com/oauth/authorize/?client_id=4d8f538893ba481f88c0614865dc9310&redirect_uri=http://127.0.0.1:8000/instagram_benchmark/login_success&response_type=token"

    return HttpResponseRedirect(url)