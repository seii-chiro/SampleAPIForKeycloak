from django.urls import path
from .views import TestView, LoginView, CallbackView, LogoutView, CustomLoginView

urlpatterns = [
    path("test/", TestView.as_view(), name="test"),
    path("login/", LoginView.as_view(), name="login"),
    path("custom_login/", CustomLoginView.as_view(), name="custom_login"),
    path("callback/", CallbackView.as_view(), name="callback"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
