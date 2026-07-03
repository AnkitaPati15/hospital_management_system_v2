from django.shortcuts import (
    get_object_or_404,
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
from rest_framework import status

from .models import Prescription
from .serializers import PrescriptionSerializer

from appointments.models import Appointment

from accounts.permission import IsDoctor


# ==================================
# FRONTEND VIEWS
# ==================================


class PrescriptionListView(ListView):

    model = Prescription

    template_name = "prescriptions/prescription_list.html"

    context_object_name = "prescriptions"

    def get_queryset(self):

        queryset = Prescription.objects.select_related(
            "appointment",
            "appointment__patient__user",
            "appointment__doctor__user",
        )

        user = self.request.user

        if user.is_authenticated:

            if user.role == "doctor":

                queryset = queryset.filter(
                    appointment__doctor__user=user
                )

            elif user.role == "patient":

                queryset = queryset.filter(
                    appointment__patient__user=user
                )

        return queryset.order_by("-created_at")


class PrescriptionCreateView(CreateView):

    model = Prescription

    fields = [
        "appointment",
        "symptoms",
        "diagnosis",
        "medicines",
        "doctor_notes",
        "follow_up_date",
    ]

    template_name = "prescriptions/prescription_form.html"

    success_url = reverse_lazy("prescription-list")

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        form.fields["appointment"].queryset = Appointment.objects.filter(
            doctor__user=self.request.user,
            status="completed",
            prescription__isnull=True,
        )

        return form


class PrescriptionUpdateView(UpdateView):

    model = Prescription

    fields = [
        "symptoms",
        "diagnosis",
        "medicines",
        "doctor_notes",
        "follow_up_date",
    ]

    template_name = "prescriptions/prescription_form.html"

    success_url = reverse_lazy("prescription-list")


class PrescriptionDeleteView(DeleteView):

    model = Prescription

    template_name = "prescriptions/prescription_confirm_delete.html"

    success_url = reverse_lazy("prescription-list")

# ==================================
# API VIEWS
# ==================================


class PrescriptionListCreateView(APIView):

    permission_classes = [IsDoctor]

    def get(self, request):

        prescriptions = Prescription.objects.select_related(
            "appointment",
            "appointment__patient__user",
            "appointment__doctor__user",
        )

        serializer = PrescriptionSerializer(
            prescriptions,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = PrescriptionSerializer(
            data=request.data
        )

        if serializer.is_valid():

            appointment = serializer.validated_data["appointment"]

            # Appointment must be completed
            if appointment.status != "completed":

                return Response(
                    {
                        "error":
                        "Prescription can only be created for completed appointments."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Doctor can create only for own appointment
            if appointment.doctor.user != request.user:

                return Response(
                    {
                        "error":
                        "You can only create prescriptions for your own appointments."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Prevent duplicate prescription
            if hasattr(
                appointment,
                "prescription"
            ):

                return Response(
                    {
                        "error":
                        "Prescription already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class PrescriptionDetailView(APIView):

    permission_classes = [IsDoctor]

    def get_object(self, pk):

        return get_object_or_404(
            Prescription,
            pk=pk,
        )

    def get(self, request, pk):

        prescription = self.get_object(pk)

        serializer = PrescriptionSerializer(
            prescription
        )

        return Response(serializer.data)

    def patch(self, request, pk):

        prescription = self.get_object(pk)

        serializer = PrescriptionSerializer(
            prescription,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):

        prescription = self.get_object(pk)

        prescription.delete()

        return Response(
            {
                "message":
                "Prescription deleted successfully."
            },
            status=status.HTTP_200_OK,
        )