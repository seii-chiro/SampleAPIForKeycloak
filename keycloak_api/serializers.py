from rest_framework import serializers
from .models import KeycloakUser


class KeycloakUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeycloakUser
        fields = [
            "keycloak_id",
            "username",
            "email",
            "given_name",
            "family_name",
            "roles",
        ]


class MeSerializer(serializers.ModelSerializer):
    patient_profile = serializers.SerializerMethodField()
    dentist_profile = serializers.SerializerMethodField()

    class Meta:
        model = KeycloakUser
        fields = [
            "keycloak_id",
            "username",
            "email",
            "given_name",
            "family_name",
            "roles",
            "patient_profile",
            "dentist_profile",
        ]

    def get_patient_profile(self, obj):
        if hasattr(obj, "patient_profile"):
            from dental_records.serializers import PatientSerializer
            return PatientSerializer(obj.patient_profile).data
        return None

    def get_dentist_profile(self, obj):
        if hasattr(obj, "dentist_profile"):
            from dental_records.serializers import DentistSerializer
            return DentistSerializer(obj.dentist_profile).data
        return None
