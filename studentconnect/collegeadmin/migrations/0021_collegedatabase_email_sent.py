# Generated by Django 5.0 on 2024-01-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0020_remove_collegedatabase_email_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegedatabase',
            name='email_sent',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
