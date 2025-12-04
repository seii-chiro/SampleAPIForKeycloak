from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from keycloak_api.custom_permission import HasRole, IsAdmin
from .models import Patient, Dentist, MedicalRecord
from django.contrib.auth import get_user_model
from .serializers import (
    PatientSerializer,
    DentistSerializer,
    MedicalRecordSerializer,
)

User = get_user_model()


# Create your views here.
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.select_related("user", "gender").prefetch_related("address")
    serializer_class = PatientSerializer
    permission_classes = [HasRole]
    required_roles = ["Standard User"]

    def perform_update(self, serializer):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        serializer.save(updated_by=user)


class DentistViewSet(ModelViewSet):
    queryset = Dentist.objects.select_related("user", "gender")
    serializer_class = DentistSerializer
    permission_classes = [HasRole]
    required_roles = ["Standard User"]

    def perform_update(self, serializer):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        serializer.save(updated_by=user)


class MedicalRecordViewSet(ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [HasRole]
    required_roles = ["Standard User"]

    def perform_create(self, serializer):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        serializer.save(updated_by=user)
