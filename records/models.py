from django.db import models
from hospital.models import Appointment
from hospital.models import Patient


class MedicalRecord(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    diagnosis = models.TextField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Record {self.id}"