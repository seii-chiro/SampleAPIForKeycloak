from django.contrib import admin
from .models import Address, Gender


# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "city_or_municipality",
        "province",
        "region",
        "postal_code",
    )
    search_fields = (
        "patient__user__username",
        "patient__user__email",
        "city_or_municipality",
        "province",
    )
    list_filter = ("region", "province")


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ("gender", "description")
    search_fields = ("gender",)
