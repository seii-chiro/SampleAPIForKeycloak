from rest_framework.routers import DefaultRouter
from .views import DentalAppointmentViewSet

router = DefaultRouter()

router.register("appointments", DentalAppointmentViewSet)

urlpatterns = router.urls
