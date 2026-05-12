from rest_framework import serializers
from .models import Bill


class BillSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='patient.user.username',
        read_only=True
    )

    doctor_name = serializers.CharField(
        source='appointment.doctor.user.username',
        read_only=True
    )

    class Meta:
        model = Bill
        fields = '__all__'