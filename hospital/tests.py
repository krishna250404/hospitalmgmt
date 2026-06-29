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


class AppointmentTests(APITestCase):

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

        self.nurse_user = User.objects.create_user(
            username="nurse1",
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

        self.nurse = Nurse.objects.create(
            user=self.nurse_user
        )

        # ---------------- APPOINTMENT ----------------

        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor1,
            nurse=self.nurse,
            appointment_date="2026-07-01T10:00:00Z"
        )

    # -------------------------------------------------

    def test_patient_can_create_appointment(self):

        self.client.force_authenticate(
            user=self.patient2_user
        )

        response = self.client.post(
            "/api/hospital/appointments/",
            {
                "doctor": self.doctor1.id,
                "nurse": self.nurse.id,
                "appointment_date": "2026-08-01T10:00:00Z"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Appointment.objects.count(),
            2
        )

    # -------------------------------------------------

    def test_doctor_cannot_create_appointment(self):

        self.client.force_authenticate(
            user=self.doctor1_user
        )

        response = self.client.post(
            "/api/hospital/appointments/",
            {
                "doctor": self.doctor1.id,
                "appointment_date": "2026-08-01T10:00:00Z"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # -------------------------------------------------

    def test_patient_sees_only_their_appointments(self):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.get(
            "/api/hospital/appointments/"
        )

        self.assertEqual(
            len(response.data),
            1
        )

        self.assertEqual(
            response.data[0]["id"],
            self.appointment.id
        )

    # -------------------------------------------------

    def test_doctor_sees_only_assigned_appointments(self):

        self.client.force_authenticate(
            user=self.doctor1_user
        )

        response = self.client.get(
            "/api/hospital/appointments/"
        )

        self.assertEqual(
            len(response.data),
            1
        )

    # -------------------------------------------------

    def test_other_doctor_cannot_update_appointment(self):

        self.client.force_authenticate(
            user=self.doctor2_user
        )

        response = self.client.patch(
            f"/api/hospital/appointments/{self.appointment.id}/",
            {
                "status": "COMPLETED"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    # -------------------------------------------------

    def test_patient_cannot_update_appointment(self):

        self.client.force_authenticate(
            user=self.patient_user
        )

        response = self.client.patch(
            f"/api/hospital/appointments/{self.appointment.id}/",
            {
                "status": "COMPLETED"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # -------------------------------------------------

    def test_doctor_can_complete_appointment(self):

        self.client.force_authenticate(
            user=self.doctor1_user
        )

        response = self.client.patch(
            f"/api/hospital/appointments/{self.appointment.id}/",
            {
                "status": "COMPLETED",
                "diagnosis": "Seasonal Flu",
                "notes": "Rest and hydration"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.appointment.refresh_from_db()

        self.assertEqual(
            self.appointment.status,
            "COMPLETED"
        )

        self.assertIsNotNone(
            self.appointment.completed_at
        )

    # -------------------------------------------------

    def test_medical_record_created(self):

        self.client.force_authenticate(
            user=self.doctor1_user
        )

        self.client.patch(
            f"/api/hospital/appointments/{self.appointment.id}/",
            {
                "status": "COMPLETED",
                "diagnosis": "Flu",
                "notes": "Medicine"
            },
            format="json"
        )

        self.assertTrue(

            MedicalRecord.objects.filter(
                appointment=self.appointment
            ).exists()

        )