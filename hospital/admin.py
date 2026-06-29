from django.contrib import admin
from .models import Doctor, Nurse, Patient, Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "nurse",
        "status",
        "appointment_date",
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )


@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )

