from rest_framework.views import APIView
from rest_framework.response import Response

from manager.choices import SERVICE_CHOICES


# Create your views here.
# =======================
class ServiceTypeView(APIView):
    def get(self, request, format=None, **kwargs):
        service_type_list = []
        for service in SERVICE_CHOICES:
            service_type_list.append({
                "value": service[0],
                "label": service[1]
            })

        return Response(service_type_list)
