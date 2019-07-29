from django.shortcuts import render
from django.views import View

from .data_provider import FacebookDataProvider


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'facebook_benchmark/login.html')

class HomeView(View):
    def get(self, request):
        return render(request, 'facebook_benchmark/home.html')