from django.contrib import admin
from .models import UserData, AuthToken


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    pass


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    pass
