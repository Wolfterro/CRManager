from rest_framework.views import APIView
from rest_framework.response import Response

from manager.models import Activity
from manager.serializers import ActivitySerializer


# Create your views here.
# =======================
class ActivityView(APIView):
    def get(self, request, format=None, **kwargs):
        if kwargs.get('pk'):
            instance = Activity.objects.filter(pk=kwargs.get('pk')).first()
            if not instance:
                return Response(
                    {"error": "A atividade com ID {} não foi encontrada!".format(kwargs.get('pk'))},
                    status=404
                )
            serializer = ActivitySerializer(instance)
        else:
            queryset = Activity.objects.all()
            serializer = ActivitySerializer(queryset, many=True)

        return Response(serializer.data)
