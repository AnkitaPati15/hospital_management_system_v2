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

from .models import Appointment
from .serializers import AppointmentSerializer
from django.urls import reverse_lazy

# ==================================

# FRONTEND VIEWS

# ==================================


class AppointmentListView(ListView):
    model = Appointment

    template_name = 'appointments/appointment_list.html'

    context_object_name = 'appointments'

    queryset = Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date')


class AppointmentCreateView(CreateView):
    model = Appointment

    fields = [
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'reason',
        'status',
    ]

    template_name = 'appointments/appointment_form.html'

    success_url = reverse_lazy('appointment-list')


class AppointmentUpdateView(UpdateView):
    model = Appointment

    fields = [
        'patient',
        'doctor',
        'appointment_date',
        'appointment_time',
        'reason',
        'status',
    ]

    template_name = 'appointments/appointment_form.html'

    success_url = reverse_lazy('appointment-list')


class AppointmentDeleteView(DeleteView):
    model = Appointment

    template_name = 'appointments/appointment_confirm_delete.html'

    success_url = reverse_lazy('appointment-list')

class BookAppointmentView(CreateView):
    model = Appointment

    fields = [
        'doctor',
        'appointment_date',
        'appointment_time',
        'reason',
    ]

    template_name = 'appointments/book_appointment.html'

    success_url = reverse_lazy('appointment-list')

    def form_valid(self, form):
        doctor = form.cleaned_data['doctor']
        appointment_date = form.cleaned_data['appointment_date']
        appointment_time = form.cleaned_data['appointment_time']

        exists = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ).exists()

        if exists:
            form.add_error(None, 'This slot is already booked.')
            return self.form_invalid(form)

        form.instance.patient = self.request.user.patient

        return super().form_valid(form)



# ==================================

# API VIEWS

# ==================================


class AppointmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Appointment, pk=pk)

    def get(self, request, pk):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def patch(self, request, pk):
        appointment = self.get_object(pk)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment = self.get_object(pk)
        appointment.status = 'cancelled'
        appointment.save()
        return Response({'message': 'Appointment cancelled successfully'})
