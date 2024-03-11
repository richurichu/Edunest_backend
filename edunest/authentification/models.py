from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from Family.models import Families


class CustomUser(AbstractUser):
    USER = 'USER'
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    BAN ='BAN'
    
    ROLE_CHOICES = [
        (USER, 'User'),
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (BAN,'Ban')
    ]
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=7,choices=ROLE_CHOICES,default=USER, blank=True,null=True)
    temp_role = models.CharField(max_length=7,choices=ROLE_CHOICES,default=USER, blank=True,null=True)
    family = models.ForeignKey(Families,on_delete=models.SET_NULL, blank=True,null=True)
    quiz_points = models.IntegerField(default=0)

    groups = models.ManyToManyField(Group, blank=True, related_name="customuser_groups")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="customuser_permissions")

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField()  
    profile_image = models.ImageField(upload_to='faculty_images/',null=True , blank=True) 
    certificate = models.FileField(upload_to='faculty_certificates/')

