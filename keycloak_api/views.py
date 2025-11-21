import requests
from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    """Redirect user to Keycloak login page"""

    permission_classes = []

    def get(self, request):
        params = {
            "client_id": settings.KEYCLOAK_AUDIENCE,
            "redirect_uri": request.build_absolute_uri("/api/callback/"),
            "response_type": "code",
            "scope": "openid profile email",
        }
        auth_url = f"{settings.KEYCLOAK_ISSUER}/protocol/openid-connect/auth?{urlencode(params)}"
        return redirect(auth_url)


class CustomLoginView(APIView):
    """
    Custom login - accepts username/password directly
    No redirect to Keycloak UI
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"}, status=400
            )

        # Request tokens directly from Keycloak using username/password
        token_url = f"{settings.KEYCLOAK_ISSUER}/protocol/openid-connect/token"
        data = {
            "grant_type": "password",
            "client_id": settings.KEYCLOAK_AUDIENCE,
            "username": username,
            "password": password,
            "scope": "openid profile email",
        }

        # If your Keycloak client requires a client secret, add it:
        # "client_secret": settings.KEYCLOAK_CLIENT_SECRET,

        try:
            response = requests.post(token_url, data=data)

            if response.status_code == 401:
                return JsonResponse(
                    {"error": "Invalid username or password"}, status=401
                )

            response.raise_for_status()
            tokens = response.json()

            return JsonResponse(
                {
                    "message": "Login successful",
                    "access_token": tokens.get("access_token"),
                    "refresh_token": tokens.get("refresh_token"),
                    "expires_in": tokens.get("expires_in"),
                    "token_type": tokens.get("token_type", "Bearer"),
                }
            )

        except requests.exceptions.RequestException as e:
            return JsonResponse(
                {"error": f"Authentication failed: {str(e)}"}, status=500
            )


class CallbackView(APIView):
    """Handle Keycloak callback and exchange code for token"""

    permission_classes = []

    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No authorization code provided"}, status=400)

        # Exchange authorization code for tokens
        token_url = f"{settings.KEYCLOAK_ISSUER}/protocol/openid-connect/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": request.build_absolute_uri("/api/callback/"),
            "client_id": settings.KEYCLOAK_AUDIENCE,
        }

        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            tokens = response.json()

            # In a real app, you'd store these tokens securely (session, cookie, etc.)
            return JsonResponse(
                {
                    "message": "Login successful!",
                    "access_token": tokens.get("access_token"),
                    "refresh_token": tokens.get("refresh_token"),
                    "expires_in": tokens.get("expires_in"),
                    "instructions": "Use the access_token in your requests: Authorization: Bearer <access_token>",
                }
            )
        except requests.exceptions.RequestException as e:
            return JsonResponse(
                {"error": f"Token exchange failed: {str(e)}"}, status=500
            )


class LogoutView(APIView):
    """Logout from Keycloak"""

    permission_classes = []

    def get(self, request):
        params = {
            "client_id": settings.KEYCLOAK_AUDIENCE,
            "post_logout_redirect_uri": request.build_absolute_uri("/api/login/"),
        }
        logout_url = f"{settings.KEYCLOAK_ISSUER}/protocol/openid-connect/logout?{urlencode(params)}"
        return redirect(logout_url)


class TestView(APIView):
    """Protected endpoint that requires authentication"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)

        return Response(
            {"user": request.user.username, "roles": getattr(request.user, "roles", [])}
        )
