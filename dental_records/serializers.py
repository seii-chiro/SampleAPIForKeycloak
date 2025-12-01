from rest_framework import serializers
from .models import Patient, Dentist, MedicalRecord
from rest_framework.exceptions import ValidationError
from keycloak_api.serializers import KeycloakUserSerializer
from core.serializers import BaseModelWithAuditTrailsSerializer, AddressSerializer


class PatientSerializer(BaseModelWithAuditTrailsSerializer):
    user = KeycloakUserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ["user", "created_by", "updated_by", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        if hasattr(user, "patient_profile"):
            raise ValidationError("Patient profile for this user already exists.")
        validated_data["user"] = user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        return super().create(validated_data)


class DentistSerializer(BaseModelWithAuditTrailsSerializer):
    user = KeycloakUserSerializer(read_only=True)

    class Meta:
        model = Dentist
        fields = "__all__"
        read_only_fields = ["user", "created_by", "updated_by", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        if hasattr(user, "dentist_profile"):
            raise ValidationError("Dentist profile for this user already exists.")
        validated_data["user"] = user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        return super().create(validated_data)


class MedicalRecordSerializer(BaseModelWithAuditTrailsSerializer):
    class Meta:
        model = MedicalRecord
        fields = "__all__"
        read_only_fields = ["date_recorded", "created_by", "updated_by", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required.")
        # patient must be provided via view or context; leave if missing
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        return super().create(validated_data)
