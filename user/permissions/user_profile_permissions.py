from rest_framework import permissions

from user.utils import get_user_profile


class UserProfilePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_profile = get_user_profile(request)
        if not user_profile:
            if request.method == "POST":
                return True

            return False

        if user_profile.user.is_superuser:
            return True

        if request.method in ["GET", "POST"]:
            return True

        pk = view.kwargs.get('pk')
        if request.method in ['PATCH', 'DELETE']:
            if pk and user_profile.pk == pk:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        user_profile = get_user_profile(request)
        if not user_profile:
            return False

        if user_profile.user.is_superuser:
            return True

        if obj.user == user_profile.user:
            return True

        return False
