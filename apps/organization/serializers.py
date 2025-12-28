from rest_framework import serializers
from .models import Organization, OrganizationMember
from apps.users.models import Users
from django.utils.text import slugify


class CreateOrganization(serializers.ModelSerializer):
    owner_user_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Organization
        fields = ["name","owner_user_id","description"]
        
    def create(self, validated_data):
        owner = Users.objects.get(id=validated_data.pop("owner_user_id"))

        slug = slugify(validated_data["name"])
        base_slug = slug
        counter = 1
        while Organization.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        org = Organization.objects.create(
            slug=slug,
            owner=owner,
            **validated_data
        )
        
        OrganizationMember.objects.create(
            organization=org,
            member=owner,
            role=OrganizationMember.Role.OWNER,
            invited_by=None 
        )
        
        return org
    

class OrganizationList(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id","name","slug","description","logo","owner"]


class UpdateOrganization(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Organization
        fields = ["name","description","logo","slug"]
        read_only_fields = ["updated_at"]
        

class OrganizationMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'member.username', read_only = True)
    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source = 'member.email', read_only = True)
    
    class Meta:
        model = OrganizationMember
        fields = [
            "id",
            "full_name",
            "username",
            "email",
            "role",  
            "joined_at"
        ]
        
    def get_full_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}"

class SendInvitationRequest(serializers.Serializer):
    sender_id = serializers.CharField()
    org_id = serializers.CharField()
    invited_username = serializers.CharField()
    
    def validate(self,data):
        try:
            org = Organization.objects.get(id=data["org_id"])
        except Organization.DoesNotExist:
            raise serializers.ValidationError("Organization does not exist.")
        
        try:
            inviting_user = Users.objects.get(id=data["sender_id"])
        except Users.DoesNotExist:
            raise serializers.ValidationError("Inviting user does not exist.")
        
        try:
            org_member = OrganizationMember.objects.get(organization=org, member=inviting_user)
        except OrganizationMember.DoesNotExist:
            raise serializers.ValidationError("You are not in this organization")
        
        allowed_roles = ["ADMIN","OWNER"]
        if org_member.role not in allowed_roles:
            raise serializers.ValidationError(
                f"User role '{org_member.role}' is not allowed to send invitations."
            )
        try:
            invited_user = Users.objects.get(username=data["invited_username"])
        except Users.DoesNotExist:
            raise serializers.ValidationError("Invited user does not exist.")
        
        data["organization"] = org
        data["inviting_user"] = inviting_user
        data["invited_user"] = invited_user

        return data
