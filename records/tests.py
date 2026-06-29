from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from hospital.models import (
    Patient,
    Doctor,
    Nurse,
    Appointment,
)
from records.models import MedicalRecord


class MedicalRecordTests(APITestCase):

    def setUp(self):

        # ---------------- USERS ----------------

        self.patient_user = User.objects.create_user(
            username="patient1",
            password="test123",
            role="PATIENT"
        )

        self.patient2_user = User.objects.create_user(
            username="patient2",
            password="test123",
            role="PATIENT"
        )

        self.doctor1_user = User.objects.create_user(
            username="doctor1",
            password="test123",
            role="DOCTOR"
        )

        self.doctor2_user = User.objects.create_user(
            username="doctor2",
            password="test123",
            role="DOCTOR"
        )

        self.nurse1_user = User.objects.create_user(
            username="nurse1",
            password="test123",
            role="NURSE"
        )

        self.nurse2_user = User.objects.create_user(
            username="nurse2",
            password="test123",
            role="NURSE"
        )

        self.admin_user = User.objects.create_user(
            username="admin",
            password="test123",
            role="ADMIN"
        )

        # ---------------- PROFILES ----------------

        self.patient = Patient.objects.create(
            user=self.patient_user,
            phone="1111111111",
            address="Delhi"
        )

        self.patient2 = Patient.objects.create(
            user=self.patient2_user,
            phone="2222222222",
            address="Mumbai"
        )

        self.doctor1 = Doctor.objects.create(
            user=self.doctor1_user,
            specialization="Cardiology"
        )

        self.doctor2 = Doctor.objects.create(
            user=self.doctor2_user,
            specialization="Neurology"
        )

        self.nurse1 = Nurse.objects.create(
            user=self.nurse1_user
        )

        self.nurse2 = Nurse.objects.create(
            user=self.nurse2_user
        )

        # ---------------- APPOINTMENT ----------------

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor1,
            nurse=self.nurse1,
            appointment_date="2026-07-01T10:00:00Z",
            status="COMPLETED",
            diagnosis="Flu",
            notes="Rest"
        )

        # Automatically created by the signal
        self.record = MedicalRecord.objects.get(
            appointment=self.appointment
        )

    # ------------------------------------------------

    def test_patient_can_view_own_record(self):

        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ------------------------------------------------

    def test_patient_cannot_view_other_patient_record(self):

        self.client.force_authenticate(user=self.patient2_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ------------------------------------------------

    def test_assigned_doctor_can_view_record(self):

        self.client.force_authenticate(user=self.doctor1_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ------------------------------------------------

    def test_other_doctor_cannot_view_record(self):

        self.client.force_authenticate(user=self.doctor2_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ------------------------------------------------

    def test_assigned_nurse_can_view_record(self):

        self.client.force_authenticate(user=self.nurse1_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ------------------------------------------------

    def test_other_nurse_cannot_view_record(self):

        self.client.force_authenticate(user=self.nurse2_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ------------------------------------------------

    def test_admin_can_view_all_records(self):

        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get("/api/records/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # ------------------------------------------------

    def test_patient_can_view_record_detail(self):

        self.client.force_authenticate(user=self.patient_user)

        response = self.client.get(
            f"/api/records/{self.record.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["diagnosis"], "Flu")