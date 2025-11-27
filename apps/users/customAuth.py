from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Users
from uuid import UUID
from rest_framework_simplejwt.settings import api_settings

class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return False
        try:
            UntypedToken(token)  
            return True
        except (InvalidToken, TokenError):
            return False




class UUIDJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Overrides the default method to handle UUID PKs
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            return Users.objects.get(id=UUID(user_id))
        except Users.DoesNotExist:
            return None

class RoleRequired(BasePermission):
    allowed_roles = []

    @classmethod
    def with_roles(cls, *roles):
        class CustomRoleRequired(cls):
            allowed_roles = roles
        return CustomRoleRequired

    def has_permission(self, request, view):
        user = request.user

        if not user or not isinstance(user, Users):
            return False

        return user.role in self.allowed_roles




