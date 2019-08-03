from django.db import models

# Create your models here.

class InstagramUser(models.Model):
    insta_uid=models.CharField(max_length=200)
    access_token=models.CharField(max_length=200)
    full_name=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    is_business = models.BooleanField(default=False)


# {'access_token': '9246763228.4d8f538.aba23cc5b7be401b93243e34819de617',
#  'user': 
#  {'id': '9246763228',
#   'username': 'az_snaps1',
#    'profile_picture': 'https://scontent.cdninstagram.com/vp/67a6db7df8b4b5ac96c1f3c7829e1d8e/5DE3C093/t51.2885-19/s150x150/44656038_560998554345667_7634009540609966080_n.jpg?_nc_ht=scontent.cdninstagram.com', 
#    'full_name': 'AZ Snaps', 
#    'bio': 'Photos that I wanted to share.', 
#    'website': '', 
#    'is_business': True}} 