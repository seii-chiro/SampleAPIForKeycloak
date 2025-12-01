from django.urls import path
from .views import (
    TestView,
    LoginView,
    CallbackView,
    LogoutView,
    CustomLoginView,
    AdminView,
    StandardUserView,
    UserViewset,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewset, basename="user")

urlpatterns = [
    path("test/", TestView.as_view(), name="test"),
    path("login/", LoginView.as_view(), name="login"),
    path("custom_login/", CustomLoginView.as_view(), name="custom_login"),
    path("callback/", CallbackView.as_view(), name="callback"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("admin_test/", AdminView.as_view(), name="admin"),
    path("standard_user_test/", StandardUserView.as_view(), name="standard_user"),
] + router.urls
