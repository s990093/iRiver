import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator

#國家清單
COUNTRY_CHOICES = (
    ('NN', '不透露'),
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('JP', 'Japan'),
    ('CN', 'China'),
    ('TW', 'Taiwan'),
    ('KR', 'Korea'),
    ('SG', 'Singapore'),
    ('MY', 'Malaysia'),
    ('TH', 'Thailand'),
    ('PH', 'Philippines'),
    ('ID', 'Indonesia'),
)
#性別清單
GENDER ={
    ('U', '不透露'),
    ('M', '男'),
    ('F', '女'),
}

#電話格式檢查
phone_test = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="電話號碼錯誤、應在9～15個數字之間 ＋號可有可無"
)
#使用者名稱格式檢查
user_test = RegexValidator(
    regex=r'^.{1,10}$',
    message="使用者名稱錯誤、應在1～10個字之間"
)
#生日格式檢查
def validate_birthday(value):
    min_date = datetime.date(1900, 1, 1)
    max_date = datetime.date.today()
    if not (min_date <= value <= max_date):
        raise ValidationError(
            _('日期錯誤，應在 %(min_date)s 到 %(max_date)s 之間'),
            params={'min_date': min_date,'max_date': max_date},
        )
#使用者資料表    
class UserProfile(models.Model):
    username = models.CharField(max_length=100, validators=[user_test])
    email = models.CharField(max_length=100, primary_key=True)
    phone = models.CharField(max_length=20,validators=[phone_test])
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    birthday = models.DateField(null=True, blank=True, validators=[validate_birthday])
    gender = models.CharField(max_length=1, choices=GENDER)