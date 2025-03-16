from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]

        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return user, validated_token
        
        except (InvalidToken, TokenError):
            return AnonymousUser(), None 
