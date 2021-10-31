from rest_framework.serializers import HyperlinkedModelSerializer

from user.models import Address


class AddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address', 'number', 'complement', 'neighborhood', 'zip_code', 'city', 'uf']