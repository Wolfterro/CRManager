from rest_framework.viewsets import ModelViewSet

from user.models import UserProfile
from user.serializers import UserProfileSerializer
from user.permissions import UserProfilePermission


# Create your viewsets here.
# ==========================
class UserProfileViewSet(ModelViewSet):
    permission_classes = [UserProfilePermission]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer