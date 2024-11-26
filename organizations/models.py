from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    is_main = models.BooleanField(default=False)
    admin = models.OneToOneField('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_organization')  

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)  

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.username
