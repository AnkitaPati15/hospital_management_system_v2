from django import forms

from .models import User

from departments.models import Department

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'role',
        ]

class DoctorRegisterForm(forms.Form):
    username = forms.CharField()

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all()
    )

    qualification = forms.CharField()

    experience = forms.IntegerField()

    consultation_fee = forms.DecimalField()

class PatientRegisterForm(forms.Form):
    username = forms.CharField()

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    age = forms.IntegerField()

    gender = forms.ChoiceField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ]
    )

    blood_group = forms.ChoiceField(
        choices=[
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-')
        ]
    )

    phone_number = forms.CharField()

    address = forms.CharField(
        widget=forms.Textarea
    )

    emergency_contact = forms.CharField()

    medical_history = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
