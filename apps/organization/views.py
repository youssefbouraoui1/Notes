from django.shortcuts import render
from rest_framework import generics
from .models import Organization, OrganizationMember
from .serializers import CreateOrganization, OrganizationList, SendInvitationRequest, UpdateOrganization
from apps.users.customAuth import IsAuthenticatedCustom, UUIDJWTAuthentication
from rest_framework.decorators import api_view
from .utils import generate_invite_token
from django_project.constants import FRONTEND_BASE_URL, ORGANIZATION_INVITATION_MAIL_SENDER
from rest_framework.response import Response
from django.core.mail import send_mail
from .pagination import OrganizationCursorPagination
from .permissions import IsOrganizationAdminOrOwner

class ListCreateOrganization(generics.ListCreateAPIView):
    queryset = Organization.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticatedCustom]
    pagination_class = OrganizationCursorPagination
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrganization
        return OrganizationList
    
    #for an upcoming task we should add basd role

class UpdateDeleteOrganization(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = UpdateOrganization
    # this will set the user and fetch
    authentication_classes = [UUIDJWTAuthentication]  
    #this will see if the token is valid
    permission_classes = [IsAuthenticatedCustom] 
    lookup_field = "id"
    
    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(
            organization_members__member = user,
            organization_members__role__in=[OrganizationMember.Role.OWNER, OrganizationMember.Role.ADMIN]
        )

    

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