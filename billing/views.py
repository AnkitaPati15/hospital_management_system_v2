from django.shortcuts import (
    get_object_or_404,
    redirect,

)

from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    View,

)
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.permission import IsAdmin

from .models import Bill
from .serializers import BillSerializer

from appointments.models import Appointment
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages



# ==================================
# FRONTEND VIEWS
# ==================================

class BillListView(ListView):

    model = Bill

    template_name = "billing/bill_list.html"

    context_object_name = "bills"

    def get_queryset(self):

        queryset = Bill.objects.select_related(
            "patient__user",
            "appointment",
            "appointment__doctor__user",
        )

        user = self.request.user

        if user.is_authenticated:

            if user.role == "patient":

                queryset = queryset.filter(
                    patient__user=user
                )

        return queryset.order_by("-created_at")


class BillCreateView(CreateView):

    model = Bill

    fields = [
        "patient",
        "appointment",
        "amount",
        "payment_status",
        "payment_method",
        "notes",
    ]

    template_name = "billing/bill_form.html"

    success_url = reverse_lazy("bill-list")

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        form.fields["appointment"].queryset = Appointment.objects.filter(
            status="completed",
            bill__isnull=True,
        )

        return form


class BillUpdateView(UpdateView):

    model = Bill

    fields = [
        "amount",
        "payment_status",
        "payment_method",
        "notes",
    ]

    template_name = "billing/bill_form.html"

    success_url = reverse_lazy("bill-list")


class BillDeleteView(DeleteView):

    model = Bill

    template_name = "billing/bill_confirm_delete.html"

    success_url = reverse_lazy("bill-list")

class MarkBillPaidView(View):

    def post(self, request, pk):

        bill = get_object_or_404(
            Bill,
            pk=pk,
        )

        if request.user.role != "admin":

            messages.error(
                request,
                "Only admin can update payment status."
            )

            return redirect("bill-list")

        bill.payment_status = "paid"

        bill.save()

        messages.success(
            request,
            "Bill marked as paid successfully."
        )

        return redirect("bill-list")    
# ==================================
# API VIEWS
# ==================================


class BillListCreateView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        bills = Bill.objects.select_related(
            "patient__user",
            "appointment",
            "appointment__doctor__user",
        )

        serializer = BillSerializer(
            bills,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = BillSerializer(
            data=request.data
        )

        if serializer.is_valid():

            appointment = serializer.validated_data["appointment"]

            # Only completed appointments
            if appointment.status != "completed":

                return Response(
                    {
                        "error":
                        "Bill can only be generated for completed appointments."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Prevent duplicate bill
            if hasattr(appointment, "bill"):

                return Response(
                    {
                        "error":
                        "Bill already exists for this appointment."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(
                patient=appointment.patient
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class BillDetailView(APIView):

    permission_classes = [IsAdmin]

    def get_object(self, pk):

        return get_object_or_404(
            Bill,
            pk=pk,
        )

    def get(self, request, pk):

        bill = self.get_object(pk)

        serializer = BillSerializer(
            bill
        )

        return Response(serializer.data)

    def patch(self, request, pk):

        bill = self.get_object(pk)

        serializer = BillSerializer(
            bill,
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

        bill = self.get_object(pk)

        bill.delete()

        return Response(
            {
                "message":
                "Bill deleted successfully."
            },
            status=status.HTTP_200_OK,
        )
