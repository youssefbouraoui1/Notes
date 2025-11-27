from rest_framework import serializers
from .models import Organization
from apps.users.models import Users
from django.utils.text import slugify


class CreateOrganization(serializers.ModelSerializer):
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
        
        return org
    

class OrganizationList(serializers.ModelSerializer):
    class Meta:
        models = Organization
        fields = ["name","slug","description","logo","owner"]