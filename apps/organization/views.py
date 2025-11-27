from django.shortcuts import render
from rest_framework import generics
from .models import Organization
from .serializers import CreateOrganization, OrganizationList
from apps.users.customAuth import IsAuthenticatedCustom

class ListCreateOrganization(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    authentication_classes = [IsAuthenticatedCustom]
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrganization
        return OrganizationList