from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from keycloak_api.custom_permission import HasRole, IsAdmin
from .models import DentalAppointment, DentalAppointmentStatus
from .serializers import DentalAppointmentSerializer, DentalAppointmentStatusSerializer


# Create your views here.
class DentalAppointmentViewSet(ModelViewSet):
    queryset = DentalAppointment.objects.select_related(
        "dentist", "patient", "appointment_status"
    )
    serializer_class = DentalAppointmentSerializer

    permission_classes = [HasRole]
    required_roles = ["Standard User"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DentalAppointmentStatusViewSet(ModelViewSet):
    queryset = DentalAppointmentStatus.objects.all()
    serializer_class = DentalAppointmentStatusSerializer

    permission_classes = [HasRole]
    required_roles = ["Standard User"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
