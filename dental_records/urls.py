from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    DentistViewSet,
    MedicalRecordViewSet,
)

router = DefaultRouter()
router.register("patients", PatientViewSet)
router.register("dentists", DentistViewSet)
router.register("medical_records", MedicalRecordViewSet)

urlpatterns = router.urls
