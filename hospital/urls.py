from django.urls import path
from .views import (
    AppointmentListCreateView,
    AppointmentUpdateView,
)


urlpatterns = [
    path(
        "appointments/",
        AppointmentListCreateView.as_view(),
        name="appointments"
    ),

    path(
        "appointments/<int:pk>/",
        AppointmentUpdateView.as_view(),
        name="appointment-detail"
    ),
]