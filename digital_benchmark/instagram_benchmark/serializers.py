from rest_framework import serializers
from .models import InstagramProfile, InstagramUserMedia, InstagramMediaInsight, InstagramMediaComments, CrawlerStats


class InstagramProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramProfile
        fields = ['created_at', 'id', 'app_user_id', 'insta_uid', 'full_name',
                  'username', 'follows_count', 'folowed_by_count', 'media_count', 'is_business']


class InstagramMediaInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMediaInsight
        fields = '__all__'


class InstagramMediaCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMediaComments
        fields = '__all__'


class InstagramUserMediaSerializer(serializers.ModelSerializer):
    comments = InstagramMediaCommentsSerializer(many=True, read_only=True)
    media_insights = serializers.SerializerMethodField()

    class Meta:
        model = InstagramUserMedia
        fields = ['id', 'created_at','insta_user_id', 'media_url',
                  'media_id', 'media_insights', 'comments']

    def get_media_insights(self, instagramMedia):
        insights = InstagramMediaInsight.objects.filter(
            id=instagramMedia.media_insight_id)
        return InstagramMediaInsightSerializer(insights, many=True).data

class CrawlerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerStats
        fields = ['status']