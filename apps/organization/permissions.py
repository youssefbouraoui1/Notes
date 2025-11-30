from rest_framework.permissions import BasePermission
from .models import OrganizationMember

class IsOrganizationAdminOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        print("DEBUG: Request user:", request.user)
        membership = obj.organization_members.filter(member=request.user).first()
        if membership is None:
            return False
        res = membership.role in [OrganizationMember.Role.OWNER, OrganizationMember.Role.ADMIN]
        print(f"res ={res}")
        return res