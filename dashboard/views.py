from multiprocessing import context

from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Bill

import json
from django.shortcuts import redirect


class AdminDashboardView(TemplateView):

    template_name = "dashboard/admin_dashboard.html"
    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
          return redirect("login-page")

        if request.user.role != "admin":
          return redirect("login-page")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        today = timezone.now().date()

        # Dashboard Counts
        context["doctor_count"] = Doctor.objects.count()
        context["patient_count"] = Patient.objects.count()
        context["appointment_count"] = Appointment.objects.count()
        context["prescription_count"] = Prescription.objects.count()
        context["bill_count"] = Bill.objects.count()

        revenue = Bill.objects.aggregate(total=Sum("amount"))
        context["total_revenue"] = revenue["total"] or 0

        # Today's Statistics
        context["today_appointments"] = Appointment.objects.filter(
            appointment_date=today
        ).count()
        context["today_schedule"] = Appointment.objects.select_related(
            "patient__user",
            "doctor__user"
        ).filter(
            appointment_date=today
        ).order_by("appointment_time")[:5]

        context["scheduled_count"] = Appointment.objects.filter(
            status="scheduled"
        ).count()

        context["completed_count"] = Appointment.objects.filter(
            status="completed"
        ).count()

        context["cancelled_count"] = Appointment.objects.filter(
            status="cancelled"
        ).count()

        # Recent Appointments
        context["recent_appointments"] = Appointment.objects.select_related(
            "patient__user",
            "doctor__user"
        ).order_by("-created_at")[:5]

        # Recent Patients
        context["recent_patients"] = Patient.objects.select_related(
            "user"
        ).order_by("-created_at")[:5]

        # Recent Doctors
        context["recent_doctors"] = Doctor.objects.select_related(
            "user"
        ).order_by("-created_at")[:5]

        # Monthly Appointment Chart
        monthly = (
            Appointment.objects
            .annotate(
                month=TruncMonth("appointment_date")
            )
            .values("month")
            .annotate(
                total=Count("id")
            )
            .order_by("month")
        )

        context["months"] = json.dumps(
            [
                item["month"].strftime("%b")
                for item in monthly
                if item["month"] is not None
            ]
        )

        context["appointment_data"] = json.dumps(
            [
                item["total"]
                for item in monthly
            ]
        )
        # Monthly Revenue

        monthly_revenue = (

            Bill.objects

            .annotate(
                month=TruncMonth("created_at")
            )

            .values("month")

            .annotate(
                total=Sum("amount")
            )

            .order_by("month")

        )

        context["revenue_months"] = json.dumps(

            [

                item["month"].strftime("%b")

                for item in monthly_revenue

                if item["month"]

            ]

        )

        context["revenue_data"] = json.dumps(

            [

                float(item["total"] or 0)

                for item in monthly_revenue

            ]

        )
        # Monthly Revenue Chart

        monthly_revenue = (
            Bill.objects
            .annotate(
                month=TruncMonth("created_at")
            )
            .values("month")
            .annotate(
                total=Sum("amount")
            )
            .order_by("month")
        )

        context["revenue_months"] = json.dumps(
            [
                item["month"].strftime("%b")
                for item in monthly_revenue
                if item["month"] is not None
            ]
        )

        context["revenue_data"] = json.dumps(
            [
                float(item["total"] or 0)
                for item in monthly_revenue
            ]
        )

        return context
class DoctorDashboardView(TemplateView):

    template_name = "dashboard/doctor_dashboard.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login-page")

        if request.user.role != "doctor":
            return redirect("login-page")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        doctor = Doctor.objects.get(user=self.request.user)

        context["appointment_count"] = Appointment.objects.filter(
            doctor=doctor
        ).count()

        context["pending_count"] = Appointment.objects.filter(
            doctor=doctor,
            status="pending"
        ).count()

        context["completed_count"] = Appointment.objects.filter(
            doctor=doctor,
            status="completed"
        ).count()

        context["today_appointments"] = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=timezone.now().date()
        ).count()

        return context       
class PatientDashboardView(TemplateView):

    template_name = "dashboard/patient_dashboard.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login-page")

        if request.user.role != "patient":
            return redirect("login-page")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        patient = Patient.objects.get(user=self.request.user)

        context["appointment_count"] = Appointment.objects.filter(
            patient=patient
        ).count()

        context["pending_count"] = Appointment.objects.filter(
            patient=patient,
            status="pending"
        ).count()

        context["completed_count"] = Appointment.objects.filter(
            patient=patient,
            status="completed"
        ).count()

        context["bill_count"] = Bill.objects.filter(
            patient=patient
        ).count()

        return context         