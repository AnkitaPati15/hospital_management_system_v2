from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    patient_name = serializers.CharField(
        source='patient.user.username',
        read_only=True
    )

    doctor_name = serializers.CharField(
        source='doctor.user.username',
        read_only=True
    )

    department_name = serializers.CharField(
        source='doctor.department.name',
        read_only=True
    )

    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):

        doctor = data['doctor']
        appointment_date = data['appointment_date']
        appointment_time = data['appointment_time']

        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='scheduled'
        ).exists()

        if existing_appointment:
            raise serializers.ValidationError(
                "Doctor already has appointment at this time."
            )

        return data