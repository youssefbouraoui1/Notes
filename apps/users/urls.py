from django.urls import path
from .views import UserListCreateUser,UserRetrieve,UserDelete,  CustomLoginView, UUIDTokenRefreshView, reset_password_request, ResetPasswordConfirmationRequest
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/refresh/',UUIDTokenRefreshView.as_view(), name='token_refresh'),
    path('',UserListCreateUser.as_view() ),
    path('<uuid:id>', UserRetrieve.as_view()),
    path('<uuid:id>/deleted',UserDelete.as_view()),
    path('auth', CustomLoginView.as_view()),
    path('reset-password', reset_password_request),
    path('confirm-reset-password', ResetPasswordConfirmationRequest)
    
]