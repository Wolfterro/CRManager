from rest_framework import permissions

from user.utils import get_user_profile


class CRPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_profile = get_user_profile(request)
        if not user_profile:
            return False

        if user_profile.user.is_superuser:
            return True

        return True

    def has_object_permission(self, request, view, obj):
        user_profile = get_user_profile(request)
        if not user_profile:
            return False

        if user_profile.user.is_superuser:
            return True

        if obj.user == user_profile:
            return True

        return False
