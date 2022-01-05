from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_designer = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    projects = models.ManyToManyField(to='Project', blank=True)


class Project(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
