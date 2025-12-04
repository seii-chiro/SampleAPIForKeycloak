from rest_framework.routers import DefaultRouter
from .views import DentalAppointmentViewSet, DentalAppointmentStatusViewSet 

router = DefaultRouter()

router.register("appointments", DentalAppointmentViewSet)
router.register("appointment-status", DentalAppointmentStatusViewSet)

urlpatterns = router.urls
