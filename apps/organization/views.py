from django.shortcuts import render
from rest_framework import generics
from .models import Organization
from .serializers import CreateOrganization, OrganizationList, SendInvitationRequest
from apps.users.customAuth import IsAuthenticatedCustom
from rest_framework.decorators import api_view
from .utils import generate_invite_token
from django_project.constants import FRONTEND_BASE_URL
from rest_framework.response import Response

class ListCreateOrganization(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    authentication_classes = [IsAuthenticatedCustom]
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrganization
        return OrganizationList
    

@api_view(["POST"])
def invite_to_organization(request):
    serializer = SendInvitationRequest(data = request.data)
    serializer.is_valid(raise_exception=True)
    
    token = generate_invite_token()
    invitation_url = f"{FRONTEND_BASE_URL}/organization/invite/{token}/"
    return Response({ "token": token, "url": invitation_url })