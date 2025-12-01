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
