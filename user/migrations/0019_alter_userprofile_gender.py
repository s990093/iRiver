# Generated by Django 4.2 on 2023-05-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_alter_userprofile_email_alter_userprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('F', '女'), ('M', '男'), ('U', '不透露')], max_length=1),
        ),
    ]
