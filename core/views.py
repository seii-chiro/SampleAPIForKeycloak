from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from keycloak_api.custom_permission import HasRole, IsAdmin
from .models import Address, Gender
from .serializers import AddressSerializer, GenderSerializer


# Create your views here.
class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [HasRole]
    required_roles = ["Standard User"]


class GenderViewSet(ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [HasRole]
    required_roles = ["Standard User"]
