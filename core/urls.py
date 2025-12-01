from rest_framework.routers import DefaultRouter
from .views import GenderViewSet, AddressViewSet

router = DefaultRouter()

router.register("address", AddressViewSet)
router.register("genders", GenderViewSet)

urlpatterns = router.urls
