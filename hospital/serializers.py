from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("patient",)

    status = serializers.ChoiceField(
    choices=Appointment.STATUS_CHOICES,
    help_text="Current appointment status."
    )