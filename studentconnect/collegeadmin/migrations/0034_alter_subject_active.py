# Generated by Django 5.0.1 on 2024-02-07 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeadmin', '0033_subject_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]