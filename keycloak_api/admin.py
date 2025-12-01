from django.contrib import admin
from .models import KeycloakUser


@admin.register(KeycloakUser)
class KeycloakUserAdmin(admin.ModelAdmin):
	list_display = (
		"username",
		"keycloak_id",
		"email",
		"given_name",
		"family_name",
		"is_staff",
		"is_active",
		"updated_at",
	)
	search_fields = ("username", "email", "keycloak_id", "given_name", "family_name")
	list_filter = ("is_staff", "is_active")
	readonly_fields = ("keycloak_id", "created_at", "updated_at")
