from django.db import models


# Create your models here.
class BaseModelWithAuditTrails(models.Model):
    created_by = models.ForeignKey(
        "keycloak_api.KeycloakUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        "keycloak_api.KeycloakUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gender(BaseModelWithAuditTrails):
    gender = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.gender


class Address(BaseModelWithAuditTrails):
    patient = models.OneToOneField(
        "dental_records.Patient", on_delete=models.CASCADE, related_name="address"
    )
    region = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city_or_municipality = models.CharField(max_length=255)
    barangay = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    @property
    def full_address(self):
        return f"{self.street}, {self.barangay}, {self.city_or_municipality}, {self.province}, {self.region} {self.postal_code}"
