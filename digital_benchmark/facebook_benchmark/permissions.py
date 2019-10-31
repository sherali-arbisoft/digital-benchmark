from rest_framework.permissions import BasePermission

class PageAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.facebook_profile.user == request.user

class PostAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.page.facebook_profile.user == request.user