# Generated by Django 5.0 on 2024-01-06 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0019_alter_collegedatabase_email_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collegedatabase',
            name='email_sent',
        ),
    ]
