# Generated by Django 4.2 on 2023-05-09 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_userprofile_country_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('U', '不透露'), ('M', '男'), ('F', '女')], max_length=1),
        ),
    ]
