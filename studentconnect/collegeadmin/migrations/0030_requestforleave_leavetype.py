# Generated by Django 5.0 on 2024-01-24 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0029_requestforleave'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestforleave',
            name='leavetype',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
