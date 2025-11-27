from rest_framework import generics,status
from .models import Users 
from .serialzers import CreateUser, UserListSeriaizer, ResetPasswordConfirmationRequest, ResetPasswordRequest
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serialzers import UUIDTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django_project.constants import PASSWORD_RESET_URL, PASSWORD_RESET_MAIL_SENDER
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from django.utils import timezone


class UserListCreateUser(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class= CreateUser
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUser
        return UserListSeriaizer
    

class UserRetrieve(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserListSeriaizer
    lookup_field='id' 
    
    
class UserDelete(generics.DestroyAPIView):
    queryset = Users.objects.all()
    lookup_field='id'
    


class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = Users.objects.get(username=username)
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
        except Users.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        access.set_exp(lifetime=timedelta(minutes=10))
        refresh.set_exp(lifetime=timedelta(days=7))

        access["username"] = user.username
        access["email"] = user.email
        access["role"] = user.role
        access["is_active"] = user.is_active
        access["user_id"] = str(user.id)

        refresh["role"] = user.role
        response = Response({
            "access": str(access),
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key= "refresh_token",
            value = str(refresh),
            httponly= True,
            secure = True,
            samesite='Strict',
            max_age=7*24*3600    
        )

        return response

    
class UUIDTokenRefreshView(TokenRefreshView):
    serializer_class = UUIDTokenRefreshSerializer


@api_view(["POST"])
def resetPasswordConfirmation(request):
    serializer = ResetPasswordConfirmationRequest(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data["user"]
    new_password = serializer.validated_data["new_password"]

    if user.check_password(new_password):
        return Response({"error": "New password must be different from the old one"}, status=status.HTTP_409_CONFLICT)
    user.set_password(new_password)
    
    user.save()

    return Response({"success": "Password updated successfully"}, status=status.HTTP_200_OK)
    

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def reset_password_request(request):
    serializer = ResetPasswordRequest(data = request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data["user"]
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    
    reset_url = f"{PASSWORD_RESET_URL}/{uidb64}/{token}"
    
    send_mail(
        subject="Reset you password",
        message=f"Click this link to reset your password {reset_url}",
        from_email= PASSWORD_RESET_MAIL_SENDER,
        recipient_list=[user.email]
    )
    return Response({"detail": "Password reset link sent to email."}, status = status.HTTP_200_OK)
