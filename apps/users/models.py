from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    class Meta:
        abstract = True


class Users(BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        DEVELOPER = 'DEVELOPER', 'Developer'
        VIEWER = 'VIEWER', 'Viewer'
    username = models.CharField(max_length=50,unique=True,null=False)
    password = models.CharField(max_length=300)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(null=True,blank=True)
    role = models.CharField(choices=Role.choices, default = Role.VIEWER)
    email = models.EmailField(unique=True,null=False)
    is_active = models.BooleanField(default = False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def get_email_field_name(self):
        return "email" 
    