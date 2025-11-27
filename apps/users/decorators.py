# users/decorators.py
from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def role_required(*allowed_roles):
    """
    Example:
        @role_required("ADMIN", "INSTRUCTOR")
        def get(self, request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # Extract role from the token payload (decoded by JWTAuthentication)
            token = getattr(request, "auth", None)
            if token is None:
                return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

            role = token.get("role") if isinstance(token, dict) else None
            if role not in allowed_roles:
                return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
