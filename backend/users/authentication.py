# authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache

class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)
        jti = validated_token.get("jti")

        if jti and cache.get(f"blacklisted_{jti}"):
            raise AuthenticationFailed("Access token has been blacklisted.")

        return validated_token
