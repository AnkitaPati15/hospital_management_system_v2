from django.db import models
from accounts.models import User
from departments.models import Department


class Doctor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='doctors'
    )

    qualification = models.CharField(
        max_length=255
    )

    experience = models.PositiveIntegerField()

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username