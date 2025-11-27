from django.shortcuts import render
from rest_framework import generics
from .models import Organization
from .serializers import CreateOrganization, OrganizationList, SendInvitationRequest
from apps.users.customAuth import IsAuthenticatedCustom
from rest_framework.decorators import api_view
from .utils import generate_invite_token
from django_project.constants import FRONTEND_BASE_URL, ORGANIZATION_INVITATION_MAIL_SENDER
from rest_framework.response import Response
from django.core.mail import send_mail

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
    user_mail = serializer.validated_data["invited_user"]
    org = serializer.validated_data["organization"]
    
    send_mail(
        subject=f"Invitation to {org.name} organization",
        message = f"Please click on this link {invitation_url} to join the organization",
        from_email= ORGANIZATION_INVITATION_MAIL_SENDER,
        recipient_list=[user_mail]
    )
    return Response({ "token": token, "url": invitation_url })