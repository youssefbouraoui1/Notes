from rest_framework import serializers
from .models import Project
from django.utils.text import slugify
from apps.organization.models import Organization


class CreateProjetSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = Project
        fiels = ['name','description','organization_id']
    
    def create(self, validated_data):
        organization = Organization.objects.get(id= validated_data.pop('organization_id'))
        return super().create(validated_data)