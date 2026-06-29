from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Appointment, Patient
from .serializers import AppointmentSerializer

from records.models import MedicalRecord

from accounts.permissions import IsDoctor

from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    tags=["Appointments"],
    summary="List or create appointments",
    description="""
Retrieve appointments visible to the authenticated user.

Permissions:

- Admin → All appointments
- Doctor → Assigned appointments
- Nurse → Assigned appointments
- Patient → Own appointments

Patients can also create new appointments.
""",
    examples=[
        OpenApiExample(
            "Create Appointment",
            request_only=True,
            value={
                "doctor": 1,
                "nurse": 1,
                "appointment_date": "2026-07-01T10:00:00Z"
            },
        ),
    ],
)
class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        print("User:", user.id, user.username, user.role)

        patient_qs = Appointment.objects.filter(
            patient__user=user
        )

        print("Appointments:", list(patient_qs.values()))

        if user.role == "ADMIN":
            return Appointment.objects.all()

        if user.role == "DOCTOR":
            return Appointment.objects.filter(
                doctor__user=user
            )

        if user.role == "NURSE":
            return Appointment.objects.filter(
                nurse__user=user
            )

        if user.role == "PATIENT":
            return patient_qs

        return Appointment.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "PATIENT":
            raise PermissionDenied(
                "Only patients can create appointments."
            )

        patient = Patient.objects.get(user=user)

        serializer.save(patient=patient)


@extend_schema(
    tags=["Appointments"],
    summary="Update appointment",
    description="""
Only the assigned doctor can update an appointment.

When the status changes from **PENDING** to **COMPLETED**, a Medical Record
is automatically created (if one does not already exist).
""",
    examples=[
        OpenApiExample(
            "Complete Appointment",
            request_only=True,
            value={
                "status": "COMPLETED",
                "diagnosis": "Seasonal Flu",
                "notes": "Rest, fluids and medication."
            },
        ),
    ],
)
class AppointmentUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Appointment.objects.filter(
            doctor__user=self.request.user
        )

    def perform_update(self, serializer):
        appointment = self.get_object()
        old_status = appointment.status

        updated_appointment = serializer.save()

        if (
            old_status != "COMPLETED"
            and updated_appointment.status == "COMPLETED"
        ):
            updated_appointment.completed_at = timezone.now()
            updated_appointment.save()

            MedicalRecord.objects.get_or_create(
                appointment=updated_appointment,
                defaults={
                    "patient": updated_appointment.patient,
                    "diagnosis": updated_appointment.diagnosis,
                    "notes": updated_appointment.notes,
                }
            )