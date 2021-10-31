from rest_framework.serializers import HyperlinkedModelSerializer

from manager.models import CR
from manager.serializers import ActivitySerializer

from user.serializers import UserProfileSerializer


class CRSerializer(HyperlinkedModelSerializer):
    user = UserProfileSerializer(required=False)
    activities = ActivitySerializer(required=False, many=True)

    class Meta:
        model = CR
        fields = ['id', 'user', 'number', 'expiration_date', 'rm', 'activities']