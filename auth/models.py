from django.db import models
import uuid
from django.utils import timezone
# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique= True)
    created_at = models.DateTimeField(default=timezone.now)
    is_activated = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"