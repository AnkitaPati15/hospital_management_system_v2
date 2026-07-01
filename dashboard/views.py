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


class AdminDashboardView(TemplateView):

    template_name = "dashboard/admin_dashboard.html"

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

        return context