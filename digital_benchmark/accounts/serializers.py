from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
