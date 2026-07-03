from django.db import models

from patients.models import Patient
from appointments.models import Appointment


class Bill(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("card", "Card"),
        ("upi", "UPI"),
    )

    bill_number = models.CharField(
        max_length=20,
        unique=True,
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="bills",
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="bill",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Bill"

        verbose_name_plural = "Bills"

    def __str__(self):

        return self.bill_number

    def save(self, *args, **kwargs):

        if not self.bill_number:

            last_bill = Bill.objects.order_by("-id").first()

            if last_bill:

                last_id = last_bill.id + 1

            else:

                last_id = 1

            self.bill_number = f"BILL{last_id:04d}"

        super().save(*args, **kwargs)