from typing import Dict, Any

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from datetime import datetime
from django.conf import settings

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add the expiration time to the response
        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        data['access_expires_at'] = (datetime.now() + access_token_lifetime).isoformat()
        data['refresh_expires_at'] = (datetime.now() + refresh_token_lifetime).isoformat()

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        # Add the expiration time to the response
        access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        data['access_expires_at'] = (datetime.now() + access_token_lifetime).isoformat()

        return data
