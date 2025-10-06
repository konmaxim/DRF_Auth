from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
class CustomUser(AbstractUser):
    username = None
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['full_name']
class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400)

class AccessRoleRule(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE) 
    element = models.ForeignKey('BusinessElement', on_delete=models.CASCADE)

    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)
    
    class Meta:
        #одно правило для каждой комбинации роли и бизнес-приложения
        unique_together = ('role', 'element')
