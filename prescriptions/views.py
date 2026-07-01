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

from .models import Prescription
from .serializers import PrescriptionSerializer
from accounts.permission import (
    IsDoctor
)

# ==================================

# FRONTEND VIEWS

# ==================================

class PrescriptionListView(ListView):
    model = Prescription

    template_name = 'prescriptions/prescription_list.html'

    context_object_name = 'prescriptions'

    queryset = Prescription.objects.select_related('appointment', 'appointment__patient', 'appointment__doctor')

class PrescriptionCreateView(CreateView):
    model = Prescription

    fields = [
        'appointment',
        'symptoms',
        'diagnosis',
        'medicines',
        'doctor_notes',
        'follow_up_date',
    ]

    template_name = 'prescriptions/prescription_form.html'

    success_url = reverse_lazy('prescription-list')

class PrescriptionUpdateView(UpdateView):
    model = Prescription

    fields = [
        'appointment',
        'symptoms',
        'diagnosis',
        'medicines',
        'doctor_notes',
        'follow_up_date',
    ]

    template_name = 'prescriptions/prescription_form.html'

    success_url = reverse_lazy('prescription-list')

class PrescriptionDeleteView(DeleteView):
    model = Prescription

    template_name = 'prescriptions/prescription_confirm_delete.html'

    success_url = reverse_lazy('prescription-list')

# ==================================

# API VIEWS

# ==================================

class PrescriptionListCreateView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        prescriptions = Prescription.objects.all()
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        if getattr(request.user, 'role', None) != 'doctor':
            return Response({'error': 'Only doctors can create prescriptions'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrescriptionDetailView(APIView):
    permission_classes = [IsDoctor]

    def get_object(self, pk):
        return get_object_or_404(Prescription, pk=pk)

    def get(self, request, pk):
        prescription = self.get_object(pk)
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)
