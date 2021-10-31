from rest_framework.serializers import ModelSerializer

from manager.models import Process
from manager.serializers import PCESerializer

from user.serializers import UserProfileSerializer


class ProcessSerializer(ModelSerializer):
    user = UserProfileSerializer(required=False)
    pce = PCESerializer(required=False)

    class Meta:
        model = Process
        fields = [
            'id',
            'user',
            'protocol',
            'entry_date',
            'entry_date_days',
            'entry_date_working_days',
            'service',
            'service_label',
            'status',
            'status_label',
            'reason',
            'om',
            'gru_status',
            'gru_status_label',
            'gru_compensation_date',
            'gru_compensation_date_days',
            'gru_compensation_date_working_days',
            'pce'
        ]
