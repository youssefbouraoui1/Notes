from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .models import Project
from .pagination import ProjectCursorPagination
from apps.users.customAuth import IsAuthenticatedCustom, UUIDJWTAuthentication

class CreateProject(CreateAPIView):
    pagination_class = ProjectCursorPagination
    permission_classes = [IsAuthenticatedCustom]
