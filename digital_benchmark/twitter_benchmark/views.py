from django.shortcuts import render
from django.http import HttpResponse
from .data_provider import DataProvider


def login(request):
    context = {'auth_url':DataProvider.get_authorization('LCE85J76ONueBmKn1SpVAjZ0F','eo992TOAXA6n9KNrKy59Qkb8uKmTMRwE3XevUHeoFm3fXihbEJ')}
    return render(request,'Login/index.html',context)


def success(request):
    #user_profile_data = DataProvider.get_user_profile_data(request.GET['oauth_verifier'],'LCE85J76ONueBmKn1SpVAjZ0F','eo992TOAXA6n9KNrKy59Qkb8uKmTMRwE3XevUHeoFm3fXihbEJ')
    #context = {'data':user_profile_data}
    return render(request,'success/index.html')


def user(request,user_id):
    return HttpResponse(user_id)
