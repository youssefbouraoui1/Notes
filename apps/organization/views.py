from django.shortcuts import render
from rest_framework import generics, status
from .models import Organization, OrganizationMember
from .serializers import CreateOrganization, OrganizationList, SendInvitationRequest, UpdateOrganization, OrganizationMemberSerializer
from apps.users.customAuth import IsAuthenticatedCustom, UUIDJWTAuthentication
from rest_framework.decorators import api_view
from .utils import generate_invite_token
from django_project.constants import FRONTEND_BASE_URL, ORGANIZATION_INVITATION_MAIL_SENDER
from rest_framework.response import Response
from django.core.mail import send_mail
from .pagination import OrganizationCursorPagination, OrganizationMemebersPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# we should only retrieve the organization that the user is related to
class ListCreateOrganization(generics.ListCreateAPIView):
    queryset = Organization.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticatedCustom]
    pagination_class = OrganizationCursorPagination
    
    def get(self, request, *args, **kwargs):
        user = request.user  
        cursor = request.GET.get("cursor", "first")
        cache_key = f"orgs:{user.id}:{cursor}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().get(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60 * 15)
        return response
    
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
    
    #normally only the admin can delete the organization
    
    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(
            organization_members__member = user,
            organization_members__role__in=[OrganizationMember.Role.OWNER, OrganizationMember.Role.ADMIN]
        )

class UpdateDeleteOrganizationBySlug(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = UpdateOrganization
    authentication_classes = [UUIDJWTAuthentication]  
    permission_classes = [IsAuthenticatedCustom] 
    lookup_field = "slug"
    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(
            organization_members__member=user,
            organization_members__role__in=[OrganizationMember.Role.OWNER, OrganizationMember.Role.ADMIN]
        )
        
    def destroy(self, request, *args, **kwargs):
        org = self.get_object()
        member = OrganizationMember.objects.get(organization=org, member=request.user)
        if member.role != OrganizationMember.Role.OWNER:
            return Response({"detail": "Only owner can delete this organization."}, status=403)
        return super().destroy(request, *args, **kwargs)
    


class ListOrganizationMembers(generics.ListAPIView):
    pagination_class = OrganizationMemebersPagination
    serializer_class = OrganizationMemberSerializer
    
    def get_queryset(self):
        slug = self.kwargs["slug"]

        return OrganizationMember.objects.filter(
            organization__slug=slug
        ).select_related("member", "organization").order_by("-joined_at")

class RemoveMemberFromOrganization(generics.DestroyAPIView):
    permission_classes = [IsAuthenticatedCustom]
    
    def get_object(self):
        member_id = self.kwargs["id"]
        slug = self.kwargs["slug"]
        
        try:
            return OrganizationMember.objects.get(
                id = member_id,
                slug=slug
            )
        except OrganizationMember.DoesNotExist:
            return None
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({"detail":"Member does not exist in this organization"}, status = 404)
        if instance.role == OrganizationMember.Role.OWNER:
            return Response({"detail": "Cannot remove the owner of the organization."}, status=403)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   

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