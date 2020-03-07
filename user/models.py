from django.db import models
from django.contrib.auth.models import AbstractUser
from group.models import Group


class User(AbstractUser):
    licence_id = models.IntegerField(null=False, blank=False)
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=30, blank=True)
    groups = models.ManyToManyField(Group)
