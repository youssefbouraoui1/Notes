from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from .models import Project
from .pagination import ProjectCursorPagination
from apps.users.customAuth import IsAuthenticatedCustom, UUIDJWTAuthentication
from .serializers import CreateProjetSerializer, ProjectSerializer

class ListCreateProject(ListCreateAPIView):
    pagination_class = ProjectCursorPagination
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    def get_serializer_class(self):
        if self.request.method =="POST":
            return CreateProjetSerializer
        return super().get_serializer_class()

class GetProjectByOrganization(ListAPIView):
    pagination_class = ProjectCursorPagination
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        orgaization_id = self.kwargs['organization_id']
        return Project.objects.get(orgaization_id= orgaization_id)
