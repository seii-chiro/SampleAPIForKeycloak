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


class Gender(models.Model):
    gender = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.gender
