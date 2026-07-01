from rest_framework import serializers

from .models import User

from doctors.models import Doctor
from patients.models import Patient

from departments.models import Department

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Doctor Fields
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False)
    qualification = serializers.CharField(required=False)
    experience = serializers.IntegerField(required=False)
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    # Patient Fields
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)
    blood_group = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    emergency_contact = serializers.CharField(required=False)
    medical_history = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
            # Doctor Fields
            'department',
            'qualification',
            'experience',
            'consultation_fee',
            # Patient Fields
            'age',
            'gender',
            'blood_group',
            'phone_number',
            'address',
            'emergency_contact',
            'medical_history',
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        role = validated_data.pop('role')

        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            role=role,
        )

        if role == 'doctor':
            Doctor.objects.create(
                user=user,
                department=validated_data.pop('department'),
                qualification=validated_data.pop('qualification'),
                experience=validated_data.pop('experience'),
                consultation_fee=validated_data.pop('consultation_fee'),
            )

        elif role == 'patient':
            Patient.objects.create(
                user=user,
                age=validated_data.pop('age'),
                gender=validated_data.pop('gender'),
                blood_group=validated_data.pop('blood_group'),
                phone_number=validated_data.pop('phone_number'),
                address=validated_data.pop('address'),
                emergency_contact=validated_data.pop('emergency_contact'),
                medical_history=validated_data.pop('medical_history', ''),
            )

        return user
