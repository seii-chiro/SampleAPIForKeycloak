from django.db import models
from core.models import BaseModelWithAuditTrails
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Patient(BaseModelWithAuditTrails):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    gender = models.ForeignKey("core.Gender", on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    office_of_assignment = models.CharField(max_length=255)
    rank = models.CharField(max_length=100)
    patient_image = models.ImageField(upload_to="patient_images/", blank=True, null=True)

    def __str__(self):
        return f"Patient: {self.user.email}"


class Dentist(BaseModelWithAuditTrails):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="dentist_profile"
    )
    gender = models.ForeignKey("core.Gender", on_delete=models.SET_NULL, null=True)
    rank = models.CharField(max_length=100)
    dentist_image = models.ImageField(upload_to="dentist_images/", blank=True, null=True)

    def __str__(self):
        return f"Dentist: {self.user.email}"


class MedicalRecord(BaseModelWithAuditTrails):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="medical_records"
    )
    date_recorded = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
