from django.db import models
from appointments.models import Appointment


class Prescription(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='prescription'
    )

    symptoms = models.TextField()

    diagnosis = models.TextField()

    medicines = models.TextField()

    doctor_notes = models.TextField(
        blank=True,
        null=True
    )

    follow_up_date = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Prescription #{self.id}"