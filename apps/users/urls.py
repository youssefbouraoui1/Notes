from django.urls import path
from .views import UserListCreateUser,UserRetrieve,UserDelete, getRandomThing, CustomLoginView, UUIDTokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',UUIDTokenRefreshView.as_view(), name='token_refresh'),
    path('',UserListCreateUser.as_view() ),
    path('<uuid:id>', UserRetrieve.as_view()),
    path('<uuid:id>/deleted',UserDelete.as_view()),
    path('random/<int:id>', getRandomThing),
    path('auth', CustomLoginView.as_view())
    
]