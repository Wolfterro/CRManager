from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

from user.models import UserProfile, Address
from user.permissions import UserProfilePermission
from user.serializers import UserProfileSerializer
from user.utils import get_user_profile
from user.errors import (COULD_NOT_FOUND_USER_WITH_ID_X,
                         CANNOT_ACCESS_USER_INFORMATION,
                         USER_IS_REQUIRED,
                         MAIN_ADDRESS_IS_REQUIRED)


# Create your views here.
# =======================
class UserProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [UserProfilePermission]

    def get(self, request, format=None, **kwargs):
        user = get_user_profile(request)

        if kwargs.get('pk'):
            instance = UserProfile.objects.filter(pk=kwargs.get('pk')).first()
            if not instance:
                return Response(
                    {"error": COULD_NOT_FOUND_USER_WITH_ID_X.format(kwargs.get('pk'))},
                    status=404
                )
            if instance != user:
                return Response(
                    {"error": CANNOT_ACCESS_USER_INFORMATION},
                    status=401
                )

            serializer = UserProfileSerializer(instance)
        else:
            queryset = UserProfile.objects.filter(id=user.id)
            serializer = UserProfileSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data

        user_data = data.pop('user', None)
        if not user_data:
            return Response({"error": USER_IS_REQUIRED}, status=400)

        address_data = data.pop('address', None)
        second_address_data = data.pop('second_address', None)
        if not address_data:
            return Response({"error": MAIN_ADDRESS_IS_REQUIRED}, status=400)

        with transaction.atomic():
            user = UserProfile.create_user(user_data)
            address = Address.objects.create(**address_data)
            second_address = Address.objects.create(**second_address_data) if second_address_data else None

            serializer = UserProfileSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                with transaction.atomic():
                    user_profile = UserProfile.objects.create(
                        user=user,
                        address=address,
                        second_address=second_address,
                        **serializer.validated_data
                    )

                    serializer = UserProfileSerializer(user_profile)
                    serializer.data['token'] = user_profile.authorization_token
                    return Response(serializer.data)

    def patch(self, request, pk):
        data = request.data
        data.pop('user', None)

        address_data = data.pop('address', None)
        second_address_data = data.pop('second_address', None)

        with transaction.atomic():
            user_profile = UserProfile.objects.get(pk=pk)

            address = Address.objects.create(**address_data) if address_data else None
            second_address = Address.objects.create(**second_address_data) if second_address_data else None

            serializer = UserProfileSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                with transaction.atomic():
                    UserProfile.objects.filter(pk=user_profile.pk).update(**serializer.validated_data)
                    user_profile.refresh_from_db()

                    if address:
                        user_profile.address = address
                    if second_address:
                        user_profile.second_address = second_address

                    user_profile.save()
                    user_profile.refresh_from_db()

                    serializer = UserProfileSerializer(user_profile)
                    return Response(serializer.data)

    def delete(self, request, pk):
        with transaction.atomic():
            user_profile = UserProfile.objects.get(pk=pk)
            user_profile.user.delete()
            user_profile.delete()

            return Response({"success": True}, status=204)
