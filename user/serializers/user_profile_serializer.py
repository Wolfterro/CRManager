from rest_framework.serializers import HyperlinkedModelSerializer

from user.models import UserProfile
from user.serializers import UserSerializer, AddressSerializer


class UserProfileSerializer(HyperlinkedModelSerializer):
    user = UserSerializer(required=False)
    address = AddressSerializer(required=False)
    second_address = AddressSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'email', 'cpf', 'birthday', 'rg', 'user', 'address', 'second_address']