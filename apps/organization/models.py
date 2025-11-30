from django.db import models

# Create your models here.

from apps.users.models import BaseModel, Users
from django.utils import timezone



class Organization(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique = True)
    description = models.TextField()
    logo = models.ImageField(upload_to='organizations_pics/', blank=True, null=True)
    owner = models.ForeignKey(Users,on_delete=models.CASCADE, related_name='owned_organizations')
    members = models.ManyToManyField(Users,through='OrganizationMember', related_name='organizations', through_fields=('organization','member'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "organizations"
    

class OrganizationMember(BaseModel):
    class Role(models.TextChoices):
        OWNER = 'OWNER','Owner'
        ADMIN = 'ADMIN','Admin'
        MEMBER = 'MEMBER','Member'
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_members')
    member = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(choices=Role.choices, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(Users, on_delete=models.SET_NULL,null=True,blank=True, related_name='invitations')
    class Meta:
        db_table = "organization_members"

class Priority(models.TextChoices):
        LOW ='LOW','Low'
        MEDUIM = 'MEDUIM', 'Meduim'
        HIGH = 'HIGH', 'High'
        CRITICAL ='CRITICAL', 'Critical'


