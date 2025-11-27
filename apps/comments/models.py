from django.db import models
from apps.users.models import Users, BaseModel
from apps.task.models import Task

# Create your models here.
class Comment(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Users, on_delete=models.CASCADE , related_name='my_own_comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
