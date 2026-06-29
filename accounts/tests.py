from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User


class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="patient1",
            password="test123",
            role="PATIENT"
        )

    def test_login_success(self):
        """
        User receives JWT access and refresh tokens.
        """

        response = self.client.post(
            "/api/token/",
            {
                "username": "patient1",
                "password": "test123"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):
        """
        Login should fail with incorrect password.
        """

        response = self.client.post(
            "/api/token/",
            {
                "username": "patient1",
                "password": "wrongpassword"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_profile_requires_authentication(self):
        """
        Anonymous users cannot access profile.
        """

        response = self.client.get(
            "/api/auth/profile/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_user_can_view_profile(self):
        """
        Logged-in users can access their profile.
        """

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            "/api/auth/profile/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "patient1"
        )

        self.assertEqual(
            response.data["role"],
            "PATIENT"
        )

    def test_profile_returns_correct_user(self):
        """
        Profile endpoint returns the logged-in user.
        """

        second_user = User.objects.create_user(
            username="doctor1",
            password="test123",
            role="DOCTOR"
        )

        self.client.force_authenticate(
            user=second_user
        )

        response = self.client.get(
            "/api/auth/profile/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["username"],
            "doctor1"
        )

        self.assertEqual(
            response.data["role"],
            "DOCTOR"
        )