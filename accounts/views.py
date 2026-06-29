from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Accounts"],
    summary="Get authenticated user's profile",
    description="""
Returns the profile information of the currently authenticated user.

Requires a valid JWT access token.

Returns:
- id
- username
- email
- role
""",
    responses=UserSerializer,
)
class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)