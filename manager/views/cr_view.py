from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

from manager.permissions import CRPermission
from manager.models import CR, Activity
from manager.serializers import CRSerializer
from manager.errors import (ERROR_NO_CR_ID_X_FOUND,
                            REQUIRES_AT_LEAST_ONE_ACTIVITY,
                            REQUIRES_AT_LEAST_ONE_VALID_ACTIVITY,
                            USER_IS_REQUIRED,
                            CR_EXISTS_FOR_USER)

from user.models import UserProfile
from user.utils import get_user_profile


# Create your views here.
# =======================
class CRView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [CRPermission]

    def get(self, request, format=None, **kwargs):
        user = get_user_profile(request)

        if kwargs.get('pk'):
            instance = CR.objects.filter(pk=kwargs.get('pk'), user=user).first()
            if not instance:
                return Response(
                    {"error": ERROR_NO_CR_ID_X_FOUND.format(kwargs.get('pk'))},
                    status=404
                )
            serializer = CRSerializer(instance)
        else:
            queryset = CR.objects.filter(user=user)
            serializer = CRSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data

        user_profile_id = data.pop('user', None)
        if not user_profile_id:
            return Response({"error": USER_IS_REQUIRED}, status=400)

        user_profile = UserProfile.objects.get(id=user_profile_id)
        if user_profile.cr_set.exists():
            return Response({"error": CR_EXISTS_FOR_USER}, status=400)

        activities_list = data.pop('activities', None)
        if not activities_list:
            return Response({"error": REQUIRES_AT_LEAST_ONE_ACTIVITY}, status=400)

        activity_instance_list = []
        for activity in activities_list:
            activity_instance = Activity.objects.filter(name=activity).first()
            if activity_instance:
                activity_instance_list.append(activity_instance)

        if not activity_instance_list:
            return Response({"error": REQUIRES_AT_LEAST_ONE_VALID_ACTIVITY}, status=400)

        serializer = CRSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                cr = CR.objects.create(user=user_profile, **serializer.validated_data)
                cr.activities.add(*[x for x in activity_instance_list])

                serializer = CRSerializer(cr)
                return Response(serializer.data, status=201)

    def patch(self, request, pk):
        data = request.data
        cr = CR.objects.get(pk=pk)

        user_profile_id = data.pop('user', None)
        if user_profile_id:
            user_profile = UserProfile.objects.get(id=user_profile_id)
        else:
            user_profile = None

        activities_list = data.pop('activities', None)
        if activities_list:
            activity_instance_list = []

            for activity in activities_list:
                activity_instance = Activity.objects.filter(name=activity).first()
                if activity_instance:
                    activity_instance_list.append(activity_instance)

            if not activity_instance_list:
                return Response({"error": REQUIRES_AT_LEAST_ONE_VALID_ACTIVITY}, status=400)
        else:
            activity_instance_list = None

        if user_profile:
            cr.user = user_profile

        with transaction.atomic():
            cr.save()
            cr.refresh_from_db()

            serializer = CRSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                CR.objects.filter(pk=pk).update(**data)
                cr.refresh_from_db()

                if activity_instance_list:
                    cr.activities.clear()
                    cr.activities.add(*[x for x in activity_instance_list])

                serializer = CRSerializer(cr)
                return Response(serializer.data, status=202)

    def delete(self, request, pk):
        with transaction.atomic():
            cr = CR.objects.get(pk=pk)
            cr.delete()

            return Response({"success": True}, status=204)
