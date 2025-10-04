from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register(request):
    data = request.data
    email = data.get('email')
    if User.objects.filter(email=email).exists():
        return Response({"error": "This email already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=email
    )
    user.set_password(data.get('password'))
    user.save()

    return Response({"email": user.email}, status=status.HTTP_201_CREATED)