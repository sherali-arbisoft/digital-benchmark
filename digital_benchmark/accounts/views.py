from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from . import json_web_token

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.views import View, generic

from .forms import UserLoginForm, UserRegisterForm


class LoginView(View):

    def get(self, request):
        form = UserLoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self, request):
        next = request.GET.get('next')
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/')
            
        return render(request,'login.html',{'form':form})
    

class RegisterView(View):

    def get(self, request):
        form = UserRegisterForm()
        return render(request,'signup.html',{'form':form})

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
            if next:
                return redirect(next)
            return redirect('/')

        return render(request,'signup.html',{'form':form})

    


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class Signup(APIView):
    def post(self, request, format=None):
        user, created = User.objects.get_or_create(username=request.data.get('username', ''), email=request.data.get('email', ''))
        if not created:
            response = {
                'error_messages': ['Username/Email Already Exists.',]
            }
        else:
            user.set_password(request.data.get('password', ''))
            user.save()
            payload = {
                'email': request.data.get('email', ''),
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
                    'Email/Password does not Match.',
                ],
            }
        else:
            payload = {
                'email': request.data.get('email', ''),
            }
            jwt = json_web_token.get_jwt(payload)
            response = {
                'success_messages': [
                    'Login Successful.',
                ],
                'jwt': jwt,
            }
        return Response(response)