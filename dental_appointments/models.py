from django.db import models
from core.models import BaseModelWithAuditTrails
from dental_records.models import Dentist, Patient
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class DentalAppointmentStatus(BaseModelWithAuditTrails):
    status = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.status


class DentalAppointment(BaseModelWithAuditTrails):
    dentist = models.ForeignKey(
        Dentist, on_delete=models.CASCADE, related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )

    date_of_appointment = models.DateTimeField()
    location = models.CharField(max_length=255)

    appointment_status = models.ForeignKey(
        DentalAppointmentStatus,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appointment_status",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="appointments_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="appointments_updated"
    )

    def __str__(self):
        return f"{self.patient.user.email} with {self.dentist.user.email} on {self.date_of_appointment}"
