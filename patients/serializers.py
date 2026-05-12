from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Patient
        fields = '__all__'