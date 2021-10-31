from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication

from manager.permissions import ProcessPermission
from manager.models import Process, PCE
from manager.serializers import ProcessSerializer

from user.models import UserProfile
from user.utils import get_user_profile


# Create your views here.
# =======================
class ProcessView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [ProcessPermission]

    def get(self, request, format=None, **kwargs):
        user = get_user_profile(request)

        if kwargs.get('pk'):
            instance = Process.objects.filter(pk=kwargs.get('pk'), user=user).first()
            if not instance:
                return Response(
                    {"error": "O processo com ID {} não foi encontrado!".format(kwargs.get('pk'))},
                    status=404
                )
            serializer = ProcessSerializer(instance)
        else:
            queryset = Process.objects.filter(user=user)
            serializer = ProcessSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        user_profile_id = data.pop('user', None)
        if not user_profile_id:
            return Response(data={"error": "É necessário um usuário!"}, status=400)

        user_profile = UserProfile.objects.get(id=user_profile_id)
        pce_data = data.pop('pce')

        with transaction.atomic():
            if pce_data:
                pce, _ = PCE.objects.get_or_create(**pce_data)
            else:
                pce = None

            serializer = ProcessSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                process = Process.objects.create(user=user_profile, **serializer.validated_data)
                if pce:
                    process.pce = pce
                    process.save()

                serializer = ProcessSerializer(process)
                return Response(serializer.data)

    def patch(self, request, pk):
        data = request.data
        process = Process.objects.get(pk=pk)

        user_profile_id = data.pop('user', None)
        if user_profile_id:
            user_profile = UserProfile.objects.get(id=user_profile_id)
        else:
            user_profile = None

        pce_data = data.pop('pce')
        pce = PCE.objects.filter(**pce_data).first() if pce_data else None

        with transaction.atomic():
            if user_profile:
                process.user = user_profile
            if pce:
                process.pce = pce

            process.save()
            process.refresh_from_db()

            serializer = ProcessSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                Process.objects.filter(pk=pk).update(**data)

                process.refresh_from_db()
                serializer = ProcessSerializer(process)
                return Response(serializer.data, status=202)

    def delete(self, request, pk):
        with transaction.atomic():
            process = Process.objects.get(pk=pk)
            process.delete()

            return Response({"success": True}, status=204)
