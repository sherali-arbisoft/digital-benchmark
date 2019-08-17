from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import json_web_token

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.views import View, generic

from .forms import UserLoginForm, UserRegisterForm

class SignupView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request,'accounts/signup.html',{'form':form})

    def post(self, request):
        next = request.GET.get('next')
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            payload = {
                'username': user.username,
            }
            jwt = json_web_token.get_jwt(payload)
            if next:
                return redirect(next, jwt=jwt)
            return redirect('home', jwt=jwt)

        return render(request,'accounts/signup.html',{'form':form})

class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request,'accounts/login.html',{'form':form})
    
    def post(self, request):
        next = request.GET.get('next')
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            payload = {
                'username': user.username,
            }
            jwt = json_web_token.get_jwt(payload)
            if next:
                return redirect(next, jwt=jwt)
            return redirect('accounts:home', jwt=jwt)
            
        return render(request,'accounts/login.html',{'form':form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self,request, jwt):
        context = {
            'jwt': jwt,
        }
        return render(request, "accounts/home.html", context)

class Signup(APIView):
    def post(self, request, format=None):
        user, created = User.objects.get_or_create(username=request.data.get('username', ''))
        if not created:
            response = {
                'error_messages': ['Username Already Exists.',]
            }
        else:
            user.set_password(request.data.get('password', ''))
            user.save()
            payload = {
                'username': request.data.get('username', ''),
            }
            jwt = json_web_token.get_jwt(payload)
            response = {
                'success_messages': ['Account Successfully Created.',],
                'jwt': jwt,
            }
        return Response(response)

class Login(APIView):
    def post(self, request, format=None):
        user = authenticate(username=request.data.get('username', ''), password=request.data.get('password', ''))
        if user is None:
            response = {
                'error_messages': [
                    'Username/Password does not Match.',
                ],
            }
        else:
            payload = {
                'username': user.username,
            }
            jwt = json_web_token.get_jwt(payload)
            response = {
                'success_messages': [
                    'Login Successful.',
                ],
                'jwt': jwt,
            }
        return Response(response)

class Home(APIView):
    def get(self, request, format=None):
        jwt = request.data.get('jwt', '')
        if not json_web_token.verify_signature(jwt):
            response = {
                'error_messages': [
                    'Invalid Signature.',
                ],
            }
        else:
            payload = json_web_token.get_payload(jwt)
            user = User.objects.get(username=payload.get('username', ''))
            response = {
                'success_messages': [
                    f'Welcome, {user.username}',
                ],
            }
        return Response(response)