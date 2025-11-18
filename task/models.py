from django.db import models
from users.models import BaseModel, Users
from organization.models import Priority
from project.models import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import  GenericForeignKey


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
    

class Comment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Users, on_delete=models.CASCADE , related_name='my_own_comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    
class Activity(BaseModel):
    class ActionType(models.TextChoices):
        CREATED = 'CREATED','Created'
        UPDATED = 'UPDATED', 'Updated'
        DELETED = 'DELETED', 'Deleted'
        COMMENTED = 'COMMENTED', 'Commented'
        ASSIGNED = 'ASSIGNED', 'Assigned'
    user = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, related_name='my_activities')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    description = models.TextField()
    metadata = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True,blank=True)


class Notification(BaseModel):
    recipient = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name='received_notifications', null=True)
    sender = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, related_name='sent_notification')
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_task = models.ForeignKey(Task,on_delete=models.SET_NULL, null=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class TimeLog(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name="time_logs", null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, related_name='time_logs', null=True)
    description = models.TextField()
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Sprint(BaseModel):
    name = models.CharField(max_length=255)