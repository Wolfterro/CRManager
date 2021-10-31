from rest_framework.serializers import HyperlinkedModelSerializer

from manager.models import Activity


class ActivitySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name']