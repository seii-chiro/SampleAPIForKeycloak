from rest_framework import serializers
from dental_records.serializers import DentistSerializer, PatientSerializer
from .models import DentalAppointment, DentalAppointmentStatus
from core.serializers import BaseModelWithAuditTrailsSerializer
from dental_records.models import Dentist, Patient


class PatientObjectAppointmentSerializer(serializers.ModelSerializer):
    full_name = serializers.SlugRelatedField(source="user", read_only=True, slug_field="full_name")

    class Meta:
        model = Patient
        fields = ["id", "full_name"]


class DentistObjectAppointmentSerializer(serializers.ModelSerializer):
    full_name = serializers.SlugRelatedField(source="user", read_only=True, slug_field="full_name")

    class Meta:
        model = Dentist
        fields = [
            "id",
            "full_name",
        ]


class DentalAppointmentStatusSerializer(BaseModelWithAuditTrailsSerializer):
    class Meta:
        model = DentalAppointmentStatus
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]


class DentalAppointmentSerializer(BaseModelWithAuditTrailsSerializer):
    dentist_detail = DentistObjectAppointmentSerializer(source="dentist", read_only=True)
    patient_detail = PatientObjectAppointmentSerializer(source="patient", read_only=True)
    appointment_status_display = serializers.StringRelatedField(
        source="appointment_status", read_only=True
    )

    class Meta:
        model = DentalAppointment
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]
