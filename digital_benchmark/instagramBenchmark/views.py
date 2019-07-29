from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('instagram benchmark app is up!')

def auth(request):
    return render(request,'auth.html',{})

def insta_login(request):
    return render(request,'firstpage.html',{})