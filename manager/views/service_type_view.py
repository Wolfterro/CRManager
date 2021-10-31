from rest_framework.views import APIView
from rest_framework.response import Response

from manager.utils import get_service_type_list


# Create your views here.
# =======================
class ServiceTypeView(APIView):
    def get(self, request, format=None, **kwargs):
        return Response(get_service_type_list())
