from rest_framework import serializers
from .models import InstagramProfile,InstagramUserMedia,InstagramMediaInsight,InstagramMediaComments
 
 
class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model=InstagramProfile
       fields=['created_at','id','app_user_id','insta_uid','full_name','username','follows_count','folowed_by_count','media_count','is_business']
 
 
class MediaInsightSerializer(serializers.ModelSerializer):
   class Meta:
       model=InstagramMediaInsight
       fields='__all__'
 
class CommentsSerializer(serializers.ModelSerializer):
   class Meta:
       model=InstagramMediaComments
       fields='__all__'
 
class MediaSerializer(serializers.ModelSerializer):
   comments=CommentsSerializer(many=True,read_only=True)
   media_insights=serializers.SerializerMethodField()
   class Meta:
       model = InstagramUserMedia
       fields = ['id','created_at','media_url','media_id','media_insights','comments']
   def get_media_insights(self,instagramMedia):
       insights=InstagramMediaInsight.objects.filter(id=instagramMedia.media_insight_id)
       return MediaInsightSerializer(insights,many=True).data
