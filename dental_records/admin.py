from django.contrib import admin
from .models import Patient, Dentist, MedicalRecord


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
    list_display = ("patient", "date_recorded", "diagnosis")
    search_fields = ("patient__user__username", "patient__user__email", "diagnosis")
    list_filter = ("date_recorded",)
    readonly_fields = ("date_recorded",)
