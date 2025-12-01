from rest_framework import serializers
from .models import Address, Gender, BaseModelWithAuditTrails


class BaseModelWithAuditTrailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModelWithAuditTrails
        fields = ["created_by", "updated_by", "created_at", "updated_at"]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class AddressSerializer(BaseModelWithAuditTrailsSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["patient"]


class GenderSerializer(BaseModelWithAuditTrailsSerializer):
    class Meta:
        model = Gender
        fields = "__all__"
