from django.shortcuts import get_object_or_404
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

from accounts.permission import IsAdmin

from .models import Doctor
from .serializers import DoctorSerializer
from django.shortcuts import render

from datetime import date

from appointments.models import Appointment
# ==================================

# FRONTEND VIEWS

# ==================================


class DoctorListView(ListView):
    model = Doctor

    template_name = 'doctors/doctor_list.html'

    context_object_name = 'doctors'

    queryset = Doctor.objects.select_related('user', 'department').order_by('user__username')


class DoctorCreateView(CreateView):
    model = Doctor

    fields = [
        'user',
        'department',
        'qualification',
        'experience',
        'consultation_fee',
        'available',
    ]

    template_name = 'doctors/doctor_form.html'

    success_url = reverse_lazy('doctor-list')


class DoctorUpdateView(UpdateView):
    model = Doctor

    fields = [
        'department',
        'qualification',
        'experience',
        'consultation_fee',
        'available',
    ]

    template_name = 'doctors/doctor_form.html'

    success_url = reverse_lazy('doctor-list')


class DoctorDeleteView(DeleteView):
    model = Doctor

    template_name = 'doctors/doctor_confirm_delete.html'

    success_url = reverse_lazy('doctor-list')


# ==================================

# API VIEWS

# ==================================


class DoctorListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        if getattr(request.user, 'role', None) != 'admin':
            return Response({'error': 'Only admin can create doctors'}, status=status.HTTP_403_FORBIDDEN)

        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DoctorDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Doctor, pk=pk)

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

def doctor_dashboard(request):

    appointments = Appointment.objects.filter(
        doctor__user=request.user
    )

    today_count = appointments.filter(
        appointment_date=date.today()
    ).count()

    pending_count = appointments.filter(
        status='scheduled'
    ).count()

    total_count = appointments.count()

    return render(

        request,

        'doctors/doctor_dashboard.html',

        {

            'appointments': appointments,

            'today_count': today_count,

            'pending_count': pending_count,

            'total_count': total_count,

        }

    )