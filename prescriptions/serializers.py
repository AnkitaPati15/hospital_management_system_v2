from rest_framework import serializers
from .models import Prescription


class PrescriptionSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='appointment.patient.user.username',
        read_only=True
    )

    doctor_name = serializers.CharField(
        source='appointment.doctor.user.username',
        read_only=True
    )

    class Meta:
        model = Prescription
        fields = '__all__'