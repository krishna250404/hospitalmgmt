from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Patient(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    def __str__(self):
        return self.user.username

class Nurse(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username

class Doctor(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    specialization = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.user.username

class Appointment(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    nurse = models.ForeignKey(
        Nurse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    appointment_date = models.DateTimeField()

    diagnosis = models.TextField(
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.patient} - {self.doctor}"

@receiver(post_save, sender=Appointment)
def create_medical_record(sender, instance, **kwargs):

    if instance.status == 'COMPLETED':

        from records.models import MedicalRecord

        MedicalRecord.objects.get_or_create(
            appointment=instance,
            defaults={
                'patient': instance.patient,
                'diagnosis': instance.diagnosis,
                'notes': instance.notes,
            }
        )