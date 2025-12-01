import requests
from jose import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", None)
        if not auth or not auth.startswith("Bearer "):
            return None

        token = auth.split()[1]

        try:
            # Get the token header to find the key ID
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            # Fetch Keycloak public keys
            jwks_response = requests.get(settings.KEYCLOAK_JWKS_URL, timeout=3).json()

            # Find the correct key
            key = None
            for jwk_key in jwks_response.get("keys", []):
                if jwk_key.get("kid") == kid:
                    key = jwk_key
                    break

            if not key:
                raise exceptions.AuthenticationFailed("Public key not found in JWKS")

            # Decode & verify token
            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=settings.KEYCLOAK_AUDIENCE,
                issuer=settings.KEYCLOAK_ISSUER,
            )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.JWTClaimsError as e:
            raise exceptions.AuthenticationFailed(f"Invalid claims: {e}")
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {e}")

        # Extract user info from claims
        keycloak_id = claims.get("sub")  # Keycloak's unique user ID
        if not keycloak_id:
            raise exceptions.AuthenticationFailed("Token missing 'sub' claim")
        username = claims.get("preferred_username", "unknown")
        given_name = claims.get("given_name", "")
        family_name = claims.get("family_name", "")
        email = claims.get("email", "")
        roles = claims.get("realm_access", {}).get("roles", [])

        # Get or create local user
        User = get_user_model()
        user, created = User.objects.get_or_create(
            keycloak_id=keycloak_id,
            defaults={
                "username": username,
                "email": email,
                "given_name": given_name,
                "family_name": family_name,
            },
        )

        # Update user info if not just created (keep data in sync)
        if not created:
            updated = False
            if user.username != username:
                # Only update if the desired username isn't taken by another user
                if not User.objects.filter(username=username).exclude(pk=user.pk).exists():
                    user.username = username
                    updated = True
            if user.email != email:
                user.email = email
                updated = True
            if user.given_name != given_name:
                user.given_name = given_name
                updated = True
            if user.family_name != family_name:
                user.family_name = family_name
                updated = True
            if user.roles != roles:
                user.roles = roles
                updated = True

            if updated:
                user.save()
        else:
            # Ensure roles persisted on initial creation if field exists
            if user.roles != roles:
                user.roles = roles
                user.save()

        # Attach Keycloak-specific data to the user object for use in views
        user.keycloak_roles = roles
        user.keycloak_claims = claims

        return (user, None)
