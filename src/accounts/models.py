from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='user_set', related_query_name='user', 
        blank=True, 
        help_text='The groups this user belongs to', verbose_name='groups')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set', related_query_name='user',
        blank=True,
        help_text='Specific permissions for this user', verbose_name='user permissions')
