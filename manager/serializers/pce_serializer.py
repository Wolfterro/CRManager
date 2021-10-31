from rest_framework.serializers import HyperlinkedModelSerializer

from manager.models import PCE


class PCESerializer(HyperlinkedModelSerializer):
    class Meta:
        model = PCE
        fields = ['id', 'name', 'manufacturer', 'pce_type', 'quantity']