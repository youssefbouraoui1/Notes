from django.shortcuts import render
from rest_framework import generics, mixins, status
from .models import Users 
from .serialzers import CreateUser, UserListSeriaizer
from rest_framework.decorators import api_view
from rest_framework import authentication
from rest_framework.response import Response
from .authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .customAuth import IsAuthenticatedCustom



# Create your views here.

class UserListCreateUser(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class= CreateUser
    permission_classes =[IsAuthenticatedCustom]
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
    
@api_view(["GET"])
def getRandomThing(request, id):
    
    return Response({"id":id}, status=status.HTTP_200_OK)

from datetime import timedelta
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = Users.objects.get(username=username)
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

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        }, status=status.HTTP_200_OK)
