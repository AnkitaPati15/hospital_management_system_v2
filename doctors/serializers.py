from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(
        source='user.username',
        read_only=True
    )

    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )

    class Meta:
        model = Doctor
        fields = '__all__'