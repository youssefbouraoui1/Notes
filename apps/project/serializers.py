from rest_framework import serializers
from .models import Project
from django.utils.text import slugify
from apps.organization.models import Organization, OrganizationMember
from apps.users.models import Users


class CreateProjetSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True)
    user_id = serializers.UUIDField(write_only = True)
    class Meta:
        model = Project
        fiels = ['name','description','organization_id','user_id']
    
    def create(self, validated_data):
        organization = Organization.objects.get(
            id=validated_data.pop('organization_id')
        )
        user = Users.objects.get(
            id=validated_data.pop('user_id')
        )

        slug = slugify(validated_data['name'])

        project = Project.objects.create(
            **validated_data,
            slug=slug,
            organization=organization,
            created_by=user
        )
        
        return project
    def validate(self,data):
        # we should validate data
        try :
            membership = OrganizationMember.objects.get(organization_id = data["organization_id"], member_id = data["user_id"])
        except OrganizationMember.DoesNotExist:
            raise serializers.ValidationError("Member does not exist")
        
        if membership.role not in [OrganizationMember.Role.OWNER, OrganizationMember.Role.ADMIN]:
            raise serializers.ValidationError(
            "Only organization owners or admins can create projects."
        )
        
        slug = slugify(data["name"])
        if Project.objects.filter(slug = slug, organization_id = data['organization_id']).exists():
            raise serializers.ValidationError("Project already exist with that slug")
        
        return data 

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'slug', 'progress_percentage','status','priority']
