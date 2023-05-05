import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
COUNTRY_CHOICES = (
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('JP', 'Japan'),
    ('CN', 'China'),
    ('TW', 'Taiwan'),
)

def validate_birthday(value):
    min_date = datetime.date(1900, 1, 1)
    max_date = datetime.date.today()
    if not (min_date <= value <= max_date):
        raise ValidationError(
            _('Invalid birthday - must be between %(min_date)s and today'),
            params={'value': value, 'min_date': min_date},
        )
class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100, primary_key=True)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    birthday = models.DateField(null=True, blank=True, validators=[validate_birthday])
