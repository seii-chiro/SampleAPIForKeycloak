from rest_framework import serializers
from dental_records.serializers import DentistSerializer, PatientSerializer
from .models import DentalAppointment, DentalAppointmentStatus
from core.serializers import BaseModelWithAuditTrailsSerializer


class DentalAppointmentStatusSerializer(BaseModelWithAuditTrailsSerializer):
    class Meta:
        model = DentalAppointmentStatus
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]


class DentalAppointmentSerializer(BaseModelWithAuditTrailsSerializer):
    dentist_detail = DentistSerializer(source="dentist", read_only=True)
    patient_detail = PatientSerializer(source="patient", read_only=True)
    appointment_status_display = serializers.StringRelatedField(
        source="appointment_status", read_only=True
    )

    class Meta:
        model = DentalAppointment
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "created_by", "updated_by"]
