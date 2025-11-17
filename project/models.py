from django.db import models
from organization.models import Organization, Priority
from users.models import Users, BaseModel

# Create your models here.
class Project(BaseModel):
    
    class Status(models.TextChoices):
        PLANNING = 'PLANNING','Planning'
        ACTIVE = 'ACTIVE', 'Active'
        ON_HOLD = 'ON HOLD', 'On Hold'
        COMPLETED = 'COMPLETED', 'Completed'
        ARCHIVED = 'ARCHIVED', 'Archived'
    
    name = models.CharField(max_length=80)
    slug = models.SlugField()
    description = models.TextField(null=True,blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name="projects")
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE,related_name="owned_projects")
    members = models.ManyToManyField(Users, through='ProjectMember', related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, default = Status.PLANNING)
    priority = models.CharField(choices=Priority.choices, default=Priority.LOW)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(decimal_places=2, max_digits=20)
    progress_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectMember(BaseModel):
    class Role(models.TextChoices):
        TEAM_LEAD = 'TEAM_LEAD','Team Lead'
        PROJECT_MANAGER = 'PROJECT_MANAGER', 'Project_Manager'
        DEVELOPER = 'DEVELOPER','Developer'
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(Users, on_delete= models.CASCADE, related_name='projects_memberships')
    role = models.CharField(choices=Role.choices, default=Role.DEVELOPER)
    