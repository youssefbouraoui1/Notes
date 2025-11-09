from django.db import models

# Create your models here.

from users.models import BaseModel, Users
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


class Project(BaseModel):
    name = models.CharField(max_length=80)
    slug = models.SlugField()
    description = models.TextField(null=True,blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name="projects")
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="owned_projects")
    members = models.ManyToManyField(Users, through='ProjectMember', related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

class ProjectMember(BaseModel):
    class Role(models.TextChoices):
        TEAM_LEAD = 'TEAM_LEAD','Team Lead'
        PROJECT_MANAGER = 'PROJECT_MANAGER', 'Project_Manager'
        DEVELOPER = 'DEVELOPER','Developer'
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(Users, on_delete= models.CASCADE, related_name='projects_memberships')
    role = models.CharField(choices=Role.choices, default=Role.DEVELOPER)