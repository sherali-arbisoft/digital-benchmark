from rest_framework import  serializers
from .models import UserTweet, UserData, OtherTweet, UserComment


class UserCommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserComment
        fields = '__all__'


class UserTweetSerializer(serializers.ModelSerializer):
    comments = UserCommentSerializers(many=True, read_only=True)

    class Meta:
        model = UserTweet
        fields = '__all__'


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


class OtherTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherTweet
        fields = '__all__'



