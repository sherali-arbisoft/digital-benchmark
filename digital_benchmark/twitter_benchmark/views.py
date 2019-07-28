from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Index Page')


def user(request,user_id):
    return HttpResponse(user_id)
