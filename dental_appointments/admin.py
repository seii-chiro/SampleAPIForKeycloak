from django.contrib import admin
from .models import DentalAppointment, DentalAppointmentStatus


@admin.register(DentalAppointment)
class DentalAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "dentist",
        "date_of_appointment",
        "location",
        "appointment_status",
        "created_at",
    )
    search_fields = (
        "patient__user__username",
        "patient__user__email",
        "dentist__user__username",
        "dentist__user__email",
        "location",
    )
    list_filter = ("appointment_status", "date_of_appointment", "created_at")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new appointment
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DentalAppointmentStatus)
class DentalAppointmentStatusAdmin(admin.ModelAdmin):
    list_display = ("status", "description")
    search_fields = ("status",)
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new status
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
