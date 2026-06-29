from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from drf_spectacular.utils import extend_schema

class MedicalRecordQuerysetMixin:

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return MedicalRecord.objects.all()

        if user.role == "PATIENT":
            return MedicalRecord.objects.filter(
                patient__user=user
            )

        if user.role == "DOCTOR":
            return MedicalRecord.objects.filter(
                appointment__doctor__user=user
            )

        if user.role == "NURSE":
            return MedicalRecord.objects.filter(
                appointment__nurse__user=user
            )

        return MedicalRecord.objects.none()
@extend_schema(
    tags=["Medical Records"],
    summary="List medical records",
    description="""
Retrieve medical records according to the authenticated user's role.

Permissions:

- Admin → All medical records
- Doctor → Records of assigned patients
- Nurse → Records of assigned patients
- Patient → Own medical records
""",
)
class MedicalRecordListView(
    MedicalRecordQuerysetMixin,
    generics.ListAPIView,
):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

@extend_schema(
    tags=["Medical Records"],
    summary="Retrieve medical record",
    description="""
Retrieve a single medical record.

The authenticated user must have permission to access the requested record.
""",
)
class MedicalRecordDetailView(
    MedicalRecordQuerysetMixin,
    generics.RetrieveAPIView,
):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]