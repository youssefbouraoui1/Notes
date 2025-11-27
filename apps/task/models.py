from django.db import models
from apps.users.models import BaseModel, Users
from apps.organization.models import Priority
from apps.project.models import Project



# Create your models here.
class Task(BaseModel):
    class Status(models.TextChoices):
        TODO = 'TODO','TODO'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        IN_REVIEW  = 'IN_REVIEW', 'In Review'
        DONE = 'DONE', 'Done'
        BLOCKED = 'BLOCKED', 'Blocked'
    class TaskType(models.TextChoices):
        BUG = 'BUG', 'Bug'
        FEATURE = 'FEATURE', 'Feature'
        IMPROVEMENT ='IMPROVEMENT', 'Improvement'
        DOCUMENTATION ='DOCUMENTATION', 'Documentation'
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(Users,on_delete=models.SET_NULL, related_name='assigned_tasks', null=True,blank=True)
    created_by = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name='created_tasks', null=True, blank = True)
    status = models.CharField(max_length=20,choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=20,choices=Priority.choices)
    estimated_hours = models.DecimalField(null=True,blank = True, decimal_places=2, max_digits=10)
    actual_hours = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    due_date = models.DateField(null =True,blank=True)
    parent_task = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True, related_name='sub_tasks')
    #tags = #it will bbe to to many tags
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True,blank = True)
    
""" class Tag(BaseModel):
    name = models.CharField(max_lentgth=50, unique = True)
    color = models.CharField()
    organization = models.ForeignKey(Organization, on_delete=models.Case, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True) """
    
class TaskAttachment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='my_attachements')
    file = models.FileField()
    uploaded_by = models.ForeignKey(Users, on_delete=models.SET_NULL,related_name='my_uploaded_attachments', null=True, blank=True)
    file_name = models.CharField(max_length=100)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


    

class Sprint(BaseModel):
    
    class Status(models.TextChoices):
        PLANNED = 'PLANNED','Planned'
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sprints")
    goal = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(choices=Status, default=Status.PLANNED)
    

class TaskSprint(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name="sprints")
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, related_name="tasks")
    added_at = models.DateTimeField(auto_now_add=True)