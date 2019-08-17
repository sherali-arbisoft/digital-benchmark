from rest_framework import serializers

from .models import FacebookProfile, Page, Post

class FacebookProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookProfile
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'