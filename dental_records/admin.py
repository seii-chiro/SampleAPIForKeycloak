from django.contrib import admin
from .models import Patient, Dentist, MedicalRecord, Address


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "date_of_birth", "rank", "office_of_assignment")
    search_fields = ("user__username", "user__email", "rank", "office_of_assignment")
    list_filter = ("gender", "rank")
    readonly_fields = ("user",)


@admin.register(Dentist)
class DentistAdmin(admin.ModelAdmin):
    list_display = ("user", "rank")
    search_fields = ("user__username", "user__email", "rank")
    list_filter = ("rank",)
    readonly_fields = ("user",)


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "date_recorded", "diagnosis", "barangay")
    search_fields = ("patient__user__username", "patient__user__email", "diagnosis")
    list_filter = ("date_recorded",)
    readonly_fields = ("date_recorded",)


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
