from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=200)