from django.db import models

from apps.users.models import BaseModel, Users
from apps.task.models import Task
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import  GenericForeignKey
from django.utils import timezone


# Create your models here.
class Activity(BaseModel):
    class ActionType(models.TextChoices):
        CREATED = 'CREATED','Created'
        UPDATED = 'UPDATED', 'Updated'
        DELETED = 'DELETED', 'Deleted'
        COMMENTED = 'COMMENTED', 'Commented'
        ASSIGNED = 'ASSIGNED', 'Assigned'
    user = models.ForeignKey(Users,on_delete=models.SET_NULL, null=True, related_name='my_activities')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=20,choices=ActionType, default=ActionType.CREATED)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    description = models.TextField()
    metadata = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)


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
