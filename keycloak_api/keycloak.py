import requests
from jose import jwt, jwk
from jose.utils import base64url_decode
from rest_framework import authentication, exceptions
from django.conf import settings


class KeycloakUser:
    """Simple user object for Keycloak-authenticated users"""
    
    def __init__(self, username, given_name, family_name, email, roles, claims):
        self.username = username
        self.given_name = given_name
        self.family_name = family_name
        self.roles = roles
        self.claims = claims
        self.email = email
        self.is_authenticated = True
        self.is_anonymous = False
    
    def __str__(self):
        return self.username


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
            jwks_response = requests.get(settings.KEYCLOAK_JWKS_URL).json()
            
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
        
        # Create a proper user object
        user = KeycloakUser(
            username=claims.get("preferred_username", "unknown"),
            given_name=claims.get("given_name", ""),
            family_name=claims.get("family_name", ""),
            email=claims.get("email", ""),
            roles=claims.get("realm_access", {}).get("roles", []),
            claims=claims
        )
        
        return (user, None)