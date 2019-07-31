# Generated by Django 2.2.3 on 2019-07-30 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_uid', models.CharField(max_length=200)),
                ('access_token', models.CharField(max_length=200)),
                ('full_name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('is_business', models.BooleanField(default=False)),
            ],
        ),
    ]
