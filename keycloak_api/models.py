from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, keycloak_id, username, email, **extra_fields):
        if not keycloak_id:
            raise ValueError("The Keycloak ID must be set")

        user = self.model(
            keycloak_id=keycloak_id,
            username=username,
            email=self.normalize_email(email) if email else "",
            **extra_fields,
        )
        user.save(using=self._db)
        return user


class KeycloakUser(AbstractBaseUser, PermissionsMixin):
    keycloak_id = models.CharField(max_length=255, unique=True, primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    given_name = models.CharField(max_length=150, blank=True)
    family_name = models.CharField(max_length=150, blank=True)
    roles = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["keycloak_id"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}".strip()
