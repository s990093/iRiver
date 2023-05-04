from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator

# Create your models here.
COUNTRY_CHOICES = (
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('JP', 'Japan'),
    ('CN', 'China'),
    ('TW', 'Taiwan'),
)

class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

