from django.shortcuts import (
get_object_or_404
)

from django.urls import reverse_lazy

from django.views.generic import (
ListView,
CreateView,
UpdateView,
DeleteView,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Patient
from .serializers import PatientSerializer
from django.views.generic import TemplateView

from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Bill
# ==================================

# FRONTEND VIEWS

# ==================================
from django.views.generic import ListView

from appointments.models import Appointment

from prescriptions.models import Prescription
from billing.models import Bill


class PatientBillListView(
    ListView
):

    model = Bill

    template_name = (
        'patients/my_bills.html'
    )

    context_object_name = (
        'bills'
    )

    def get_queryset(self):

        return Bill.objects.filter(

            patient=
            self.request.user.patient

        )


class PatientPrescriptionListView(
    ListView
):

    model = Prescription

    template_name = (
        'patients/my_prescriptions.html'
    )

    context_object_name = (
        'prescriptions'
    )

    def get_queryset(self):

        return Prescription.objects.filter(

            appointment__patient=
            self.request.user.patient

        ).select_related(

            'appointment',
            'appointment__doctor',
            'appointment__doctor__user'

        )


class PatientAppointmentListView(
    ListView
):

    model = Appointment

    template_name = (
        'patients/my_appointments.html'
    )

    context_object_name = (
        'appointments'
    )

    def get_queryset(self):

        return Appointment.objects.filter(

            patient=
            self.request.user.patient

        ).select_related(

            'doctor',
            'doctor__user'

        )

class PatientListView(ListView):
    model = Patient

    template_name = 'patients/patient_list.html'

    context_object_name = 'patients'

    queryset = Patient.objects.select_related('user').order_by('user__username')


class PatientCreateView(CreateView):
    model = Patient

    fields = [
        'user',
        'age',
        'gender',
        'blood_group',
        'phone_number',
        'address',
        'emergency_contact',
        'medical_history',
    ]

    template_name = 'patients/patient_form.html'

    success_url = reverse_lazy('patient-list')


class PatientUpdateView(UpdateView):
    model = Patient

    fields = [
        'age',
        'gender',
        'blood_group',
        'phone_number',
        'address',
        'emergency_contact',
        'medical_history',
    ]

    template_name = 'patients/patient_form.html'

    success_url = reverse_lazy('patient-list')


class PatientDeleteView(DeleteView):
    model = Patient

    template_name = 'patients/patient_confirm_delete.html'

    success_url = reverse_lazy('patient-list')


# ==================================

# API VIEWS

# ==================================


class PatientListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        if getattr(request.user, 'role', None) != 'admin':
            return Response({'error': 'Only admin can create patients'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Patient, pk=pk)

    def get(self, request, pk):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
class PatientDashboardView(
    TemplateView
):

    template_name = (
        'patients/patient_dashboard.html'
    )

    def get_context_data(
        self,
        **kwargs
    ):

        context = super().get_context_data(
            **kwargs
        )

        patient = (
            self.request.user.patient
        )

        context[
            'appointment_count'
        ] = Appointment.objects.filter(
            patient=patient
        ).count()

        context[
            'prescription_count'
        ] = Prescription.objects.filter(
            appointment__patient=patient
        ).count()

        context[
            'bill_count'
        ] = Bill.objects.filter(
            patient=patient
        ).count()

        return context    
